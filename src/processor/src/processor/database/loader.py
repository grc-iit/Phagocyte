"""LanceDB loading and indexing."""

import contextlib
import json
from datetime import datetime
from pathlib import Path

import lancedb

from ..config import DatabaseConfig
from ..types import Chunk, ContentType, ImageChunk


class LanceDBLoader:
    """Load chunks into LanceDB with automatic indexing.

    Paths are stored as relative to input_root for portability.
    The input_root is stored in the _metadata table so paths can be
    reconstructed when the database is loaded on a different machine.
    """

    METADATA_TABLE = "_metadata"

    def __init__(
        self,
        uri: str = "./lancedb",
        text_table: str = "text_chunks",
        code_table: str = "code_chunks",
        image_table: str = "image_chunks",
        unified_table: str = "chunks",
        table_mode: str = "separate",
        text_dims: int = 1024,
        code_dims: int = 768,
        image_text_dims: int = 1024,
        image_visual_dims: int = 1024,
        input_root: Path | None = None,
    ):
        """Initialize loader.

        Args:
            uri: LanceDB database path
            text_table: Name for text chunks table
            code_table: Name for code chunks table
            image_table: Name for image chunks table
            unified_table: Name for unified chunks table
            table_mode: 'separate', 'unified', or 'both'
            text_dims: Dimensions for text embeddings
            code_dims: Dimensions for code embeddings
            image_text_dims: Dimensions for image text embeddings
            image_visual_dims: Dimensions for image visual embeddings
            input_root: Root directory for relative path calculation (portability)
        """
        self.uri = uri
        self.text_table_name = text_table
        self.code_table_name = code_table
        self.image_table_name = image_table
        self.unified_table_name = unified_table
        self.table_mode = table_mode
        self.text_dims = text_dims
        self.code_dims = code_dims
        self.image_text_dims = image_text_dims
        self.image_visual_dims = image_visual_dims
        self.input_root = input_root
        self._db: lancedb.DBConnection | None = None

    @classmethod
    def from_config(
        cls,
        config: DatabaseConfig,
        input_root: Path | None = None,
    ) -> "LanceDBLoader":
        """Create loader from config.

        Args:
            config: Database configuration
            input_root: Root directory for relative path calculation (portability)

        Returns:
            Configured LanceDBLoader instance
        """
        return cls(
            uri=config.uri,
            text_table=config.text_table,
            code_table=config.code_table,
            image_table=getattr(config, "image_table", "image_chunks"),
            unified_table=config.unified_table,
            table_mode=config.table_mode,
            input_root=input_root,
        )

    def connect(self) -> lancedb.DBConnection:
        """Connect to LanceDB."""
        if self._db is None:
            # Create directory if needed
            Path(self.uri).mkdir(parents=True, exist_ok=True)
            self._db = lancedb.connect(self.uri)
        return self._db

    def _to_relative_path(self, path: str | Path) -> str:
        """Convert absolute path to relative path for portability.

        If input_root is set, paths are made relative to it.
        Otherwise, paths are stored as-is (for backwards compatibility).

        Args:
            path: Absolute or relative path

        Returns:
            Relative path string (uses forward slashes for cross-platform)
        """
        if self.input_root is None:
            return str(path)

        path_obj = Path(path)
        try:
            relative = path_obj.relative_to(self.input_root)
            # Use forward slashes for cross-platform compatibility
            return str(relative).replace("\\", "/")
        except ValueError:
            # Path is not under input_root, store as-is
            return str(path)

    def _save_metadata(self) -> None:
        """Save database metadata for portability."""
        db = self.connect()

        metadata_records = [
            {"key": "input_root", "value": str(self.input_root) if self.input_root else ""},
            {"key": "created_at", "value": datetime.utcnow().isoformat()},
            {"key": "processor_version", "value": "1.0.0"},
        ]

        if self.METADATA_TABLE in db.table_names():
            # Update existing metadata
            db.open_table(self.METADATA_TABLE)
            # Replace all records
            db.drop_table(self.METADATA_TABLE)
            db.create_table(self.METADATA_TABLE, metadata_records)
        else:
            db.create_table(self.METADATA_TABLE, metadata_records)

    def get_metadata(self) -> dict[str, str]:
        """Get database metadata.

        Returns:
            Dictionary of metadata key-value pairs
        """
        db = self.connect()

        if self.METADATA_TABLE not in db.table_names():
            return {}

        table = db.open_table(self.METADATA_TABLE)
        records = table.to_pandas()
        return dict(zip(records["key"], records["value"], strict=False))

    async def load_chunks(
        self,
        chunks: list[Chunk],
        create_index: bool = True,
    ) -> dict[str, int]:
        """Load chunks into appropriate tables.

        Args:
            chunks: Chunks with embeddings attached
            create_index: Whether to create/update indices

        Returns:
            Dictionary with counts per table
        """
        db = self.connect()

        # Save metadata on first load (for path portability)
        if self.METADATA_TABLE not in db.table_names():
            self._save_metadata()

        # Separate chunks by type
        text_chunks = []
        code_chunks = []

        for chunk in chunks:
            if chunk.source_type.value.startswith("code_"):
                code_chunks.append(chunk)
            else:
                text_chunks.append(chunk)

        result = {"text_chunks": 0, "code_chunks": 0, "unified_chunks": 0}

        # Load into separate tables
        if self.table_mode in ("separate", "both"):
            if text_chunks:
                count = self._load_text_chunks(db, text_chunks)
                result["text_chunks"] = count

            if code_chunks:
                count = self._load_code_chunks(db, code_chunks)
                result["code_chunks"] = count

        # Load into unified table
        if self.table_mode in ("unified", "both"):
            all_chunks = text_chunks + code_chunks
            if all_chunks:
                count = self._load_unified_chunks(db, all_chunks)
                result["unified_chunks"] = count

        # Create indices
        if create_index:
            await self.create_indices()

        return result

    def _load_text_chunks(self, db: lancedb.DBConnection, chunks: list[Chunk]) -> int:
        """Load text chunks into text table."""
        records = [self._chunk_to_text_record(c) for c in chunks]

        if self.text_table_name in db.table_names():
            table = db.open_table(self.text_table_name)
            table.add(records)
        else:
            db.create_table(self.text_table_name, records)

        return len(records)

    def _load_code_chunks(self, db: lancedb.DBConnection, chunks: list[Chunk]) -> int:
        """Load code chunks into code table."""
        records = [self._chunk_to_code_record(c) for c in chunks]

        if self.code_table_name in db.table_names():
            table = db.open_table(self.code_table_name)
            table.add(records)
        else:
            db.create_table(self.code_table_name, records)

        return len(records)

    def _load_unified_chunks(self, db: lancedb.DBConnection, chunks: list[Chunk]) -> int:
        """Load all chunks into unified table."""
        records = [self._chunk_to_unified_record(c) for c in chunks]

        if self.unified_table_name in db.table_names():
            table = db.open_table(self.unified_table_name)
            table.add(records)
        else:
            db.create_table(self.unified_table_name, records)

        return len(records)

    async def load_image_chunks(
        self,
        image_chunks: list[ImageChunk],
        create_index: bool = True,
    ) -> dict[str, int]:
        """Load image chunks into the image table.

        Image chunks have dual embeddings:
        - text_vector: From VLM description
        - visual_vector: From CLIP/SigLIP

        Args:
            image_chunks: ImageChunks with embeddings attached
            create_index: Whether to create/update indices

        Returns:
            Dictionary with counts
        """
        db = self.connect()
        result = {"image_chunks": 0}

        if not image_chunks:
            return result

        # Load into image table (always separate, images have dual embeddings)
        records = [self._image_chunk_to_record(c) for c in image_chunks]

        if self.image_table_name in db.table_names():
            table = db.open_table(self.image_table_name)
            table.add(records)
        else:
            db.create_table(self.image_table_name, records)

        result["image_chunks"] = len(records)

        # Create indices
        if create_index and len(records) >= 256:
            await self._create_image_indices()

        return result

    async def _create_image_indices(self) -> None:
        """Create indices on image table (both vectors)."""
        db = self.connect()

        if self.image_table_name not in db.table_names():
            return

        table = db.open_table(self.image_table_name)
        row_count = table.count_rows()

        if row_count < 256:
            return

        # Create IVF-PQ index on text_vector
        with contextlib.suppress(Exception):
            table.create_index(
                metric="L2",
                num_partitions=min(256, row_count // 10),
                num_sub_vectors=96,
                vector_column_name="text_vector",
            )

        # Create IVF-PQ index on visual_vector
        with contextlib.suppress(Exception):
            table.create_index(
                metric="L2",
                num_partitions=min(256, row_count // 10),
                num_sub_vectors=96,
                vector_column_name="visual_vector",
            )

        # Create FTS index on VLM description
        with contextlib.suppress(Exception):
            table.create_fts_index("vlm_description")

    def _image_chunk_to_record(self, chunk: ImageChunk) -> dict:
        """Convert ImageChunk to image table record.

        Image paths are stored as relative to input_root for portability.
        """
        return {
            "id": chunk.id,
            "figure_id": chunk.figure_id,
            "caption": chunk.caption,
            "vlm_description": chunk.vlm_description,
            "classification": chunk.classification,
            "page": chunk.page,
            "image_path": self._to_relative_path(chunk.image_path),
            "source_paper": chunk.source_paper,
            "text_vector": chunk.text_embedding,
            "visual_vector": chunk.visual_embedding,
        }

    def _chunk_to_text_record(self, chunk: Chunk) -> dict:
        """Convert Chunk to text table record.

        Source file paths are stored as relative to input_root for portability.
        """
        return {
            "id": chunk.id,
            "content": chunk.content,
            "content_hash": chunk.content_hash,
            "vector": chunk.embedding,
            "source_file": self._to_relative_path(chunk.source_file),
            "source_type": chunk.source_type.value,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
            "parent_id": chunk.parent_id,
            "title": chunk.title,
            "section_path": chunk.section_path,
            "citations": json.dumps(chunk.citations) if chunk.citations else None,
            "token_count": chunk.token_count,
        }

    def _chunk_to_code_record(self, chunk: Chunk) -> dict:
        """Convert Chunk to code table record.

        Source file paths are stored as relative to input_root for portability.
        """
        return {
            "id": chunk.id,
            "content": chunk.content,
            "content_hash": chunk.content_hash,
            "vector": chunk.embedding,
            "source_file": self._to_relative_path(chunk.source_file),
            "source_type": chunk.source_type.value,
            "language": chunk.language,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
            "parent_id": chunk.parent_id,
            "symbol_name": chunk.symbol_name,
            "symbol_type": chunk.symbol_type,
            "imports": json.dumps(chunk.imports) if chunk.imports else None,
            "token_count": chunk.token_count,
        }

    def _chunk_to_unified_record(self, chunk: Chunk) -> dict:
        """Convert Chunk to unified table record.

        Source file paths are stored as relative to input_root for portability.
        """
        # Determine content type category
        if chunk.source_type.value.startswith("code_"):
            content_type = "code"
        elif chunk.source_type == ContentType.PAPER:
            content_type = "paper"
        else:
            content_type = "text"

        # Build metadata JSON
        metadata = {}
        if chunk.citations:
            metadata["citations"] = chunk.citations
        if chunk.imports:
            metadata["imports"] = chunk.imports

        return {
            "id": chunk.id,
            "content": chunk.content,
            "content_hash": chunk.content_hash,
            "vector": chunk.embedding,
            "source_file": self._to_relative_path(chunk.source_file),
            "source_type": chunk.source_type.value,
            "content_type": content_type,
            "language": chunk.language,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "parent_id": chunk.parent_id,
            "title": chunk.title,
            "section_path": chunk.section_path,
            "symbol_name": chunk.symbol_name,
            "symbol_type": chunk.symbol_type,
            "metadata_json": json.dumps(metadata) if metadata else None,
            "token_count": chunk.token_count,
        }

    async def create_indices(
        self,
        ivf_partitions: int = 256,
    ) -> None:
        """Create vector and FTS indices on tables."""
        db = self.connect()

        for table_name in [self.text_table_name, self.code_table_name, self.unified_table_name]:
            if table_name not in db.table_names():
                continue

            table = db.open_table(table_name)
            row_count = table.count_rows()

            # Create FTS index on content (always, needed for hybrid search)
            with contextlib.suppress(Exception):
                table.create_fts_index("content")

            # Create IVF-PQ vector index (only for larger tables)
            if row_count >= 256:
                with contextlib.suppress(Exception):
                    table.create_index(
                        num_partitions=min(ivf_partitions, row_count // 10),
                        num_sub_vectors=96,
                    )

    def get_stats(self) -> dict[str, int]:
        """Get row counts for all tables."""
        db = self.connect()
        stats = {}

        for table_name in db.table_names():
            table = db.open_table(table_name)
            stats[table_name] = table.count_rows()

        return stats
