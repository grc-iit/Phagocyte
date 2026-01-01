"""Core types for the processor package."""

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class ContentType(Enum):
    """Content types for chunking strategy selection."""

    # Code types
    CODE_CPP = "code_cpp"
    CODE_PYTHON = "code_python"
    CODE_SHELL = "code_shell"
    CODE_JAVA = "code_java"
    CODE_JS = "code_js"
    CODE_TS = "code_ts"
    CODE_GO = "code_go"
    CODE_RUST = "code_rust"
    CODE_OTHER = "code_other"

    # Document types
    PAPER = "paper"
    WEBSITE = "website"
    MARKDOWN = "markdown"
    TEXT = "text"

    # Multimodal types
    IMAGE = "image"

    # Future extensibility
    BOOK = "book"
    YOUTUBE = "youtube"


class EmbeddingProfile(Enum):
    """Embedding model profiles."""

    LOW = "low"
    LOW_LONG = "low-long"
    HIGH = "high"


@dataclass
class Chunk:
    """Represents a processed chunk of content."""

    id: str
    content: str
    content_hash: str
    source_file: str
    source_type: ContentType

    # Position metadata
    start_line: int | None = None
    end_line: int | None = None
    start_char: int | None = None
    end_char: int | None = None
    parent_id: str | None = None

    # Semantic metadata
    title: str | None = None
    section_path: str | None = None
    language: str | None = None

    # Code-specific metadata
    symbol_name: str | None = None
    symbol_type: str | None = None
    imports: list[str] = field(default_factory=list)

    # Paper-specific metadata
    citations: list[str] = field(default_factory=list)

    # Processing metadata
    token_count: int | None = None
    embedding: list[float] | None = None

    def compute_hash(self) -> str:
        """Compute content hash for deduplication."""
        return hashlib.sha256(self.content.encode()).hexdigest()[:16]

    @classmethod
    def create(
        cls,
        content: str,
        source_file: str | Path,
        source_type: ContentType,
        **kwargs: Any,
    ) -> "Chunk":
        """Factory method to create a chunk with auto-generated ID and hash.

        ID format: filename:line:hash (portable, not tied to absolute paths)
        """
        source_path = Path(source_file) if isinstance(source_file, str) else source_file
        source_str = str(source_file)
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

        # Generate unique ID from filename (not full path) and content hash
        # This makes IDs portable across machines
        start_line = kwargs.get("start_line", 0)
        chunk_id = f"{source_path.name}:{start_line}:{content_hash[:8]}"

        return cls(
            id=chunk_id,
            content=content,
            content_hash=content_hash,
            source_file=source_str,
            source_type=source_type,
            **kwargs,
        )


@dataclass
class ProcessingResult:
    """Result of processing a single file."""

    source_file: str
    content_type: ContentType
    chunks: list[Chunk]
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def success(self) -> bool:
        return not self.has_errors and self.chunk_count > 0


@dataclass
class ProcessingState:
    """Tracks processing state for incremental updates."""

    processed_files: dict[str, str] = field(default_factory=dict)  # path -> content_hash
    last_run: str | None = None
    version: str = "1.0.0"

    def needs_processing(self, path: Path) -> bool:
        """Check if file needs (re)processing."""
        current_hash = self._file_hash(path)
        stored_hash = self.processed_files.get(str(path))
        return current_hash != stored_hash

    def mark_processed(self, path: Path) -> None:
        """Mark file as processed."""
        self.processed_files[str(path)] = self._file_hash(path)

    def _file_hash(self, path: Path) -> str:
        """Compute file content hash."""
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


@dataclass
class ImageChunk:
    """Represents an image from a paper with VLM metadata.

    Images are processed differently from text chunks:
    - They have both text embedding (from VLM description) AND visual embedding (from CLIP)
    - The caption and description come from figures.json metadata
    - No chunking is done - one ImageChunk per figure
    """

    id: str
    figure_id: int
    caption: str
    vlm_description: str
    classification: str  # e.g., "bar_chart (1.00)", "line_chart (0.95)"
    page: int
    image_path: Path
    source_paper: str  # Directory name of the source paper

    # Embeddings (set during processing)
    text_embedding: list[float] | None = None  # From VLM description via stella/Qwen
    visual_embedding: list[float] | None = None  # From CLIP/SigLIP

    @property
    def searchable_text(self) -> str:
        """Combined text for text embedding (caption + VLM description)."""
        parts = []
        if self.caption:
            parts.append(self.caption)
        if self.vlm_description:
            parts.append(self.vlm_description)
        return "\n\n".join(parts)

    @property
    def is_logo(self) -> bool:
        """Check if this figure is classified as a logo (should be skipped)."""
        return "logo" in self.classification.lower()

    @classmethod
    def from_figure_json(
        cls,
        figure_data: dict[str, Any],
        paper_dir: Path,
    ) -> "ImageChunk":
        """Create ImageChunk from figures.json entry.

        Args:
            figure_data: Single figure entry from figures.json
            paper_dir: Path to the paper directory

        Returns:
            ImageChunk instance
        """
        figure_id = figure_data.get("figure_id", 0)
        image_path_str = figure_data.get("image_path", "")

        # Resolve image path relative to paper directory
        if image_path_str.startswith("./"):
            image_path_str = image_path_str[2:]
        image_path = paper_dir / image_path_str

        # Generate unique ID
        chunk_id = f"{paper_dir.name}:fig{figure_id}"

        return cls(
            id=chunk_id,
            figure_id=figure_id,
            caption=figure_data.get("caption", ""),
            vlm_description=figure_data.get("description", ""),
            classification=figure_data.get("classification", ""),
            page=figure_data.get("page", 0),
            image_path=image_path,
            source_paper=paper_dir.name,
        )


@dataclass
class ImageProcessingResult:
    """Result of processing images from a paper."""

    source_paper: str
    image_chunks: list[ImageChunk]
    errors: list[str] = field(default_factory=list)

    @property
    def chunk_count(self) -> int:
        return len(self.image_chunks)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def success(self) -> bool:
        return not self.has_errors
