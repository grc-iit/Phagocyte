"""Main processing pipeline."""

import json
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from ..chunkers.factory import ChunkerFactory
from ..config import ProcessorConfig
from ..core.detector import ContentDetector
from ..core.router import ContentRouter
from ..database.loader import LanceDBLoader
from ..embedders.base import BaseEmbedder
from ..embedders.ollama import OllamaEmbedder
from ..embedders.profiles import EmbedderBackend, get_model_for_profile
from ..images.processor import ImageProcessor
from ..types import Chunk, ContentType, ImageChunk, ProcessingResult, ProcessingState

console = Console()


class Pipeline:
    """Main processing pipeline orchestrating chunking, embedding, and loading."""

    def __init__(self, config: ProcessorConfig):
        """Initialize pipeline with configuration.

        Args:
            config: Processor configuration
        """
        self.config = config
        self.detector = ContentDetector(
            directory_map=config.content_mapping.model_dump()
        )
        self.router = ContentRouter(self.detector)
        self.chunker_factory = ChunkerFactory(config.chunking)
        self.image_processor = ImageProcessor(skip_logos=True)
        self.state = self._load_state()

        # Determine backend from config (default: Ollama)
        backend_str = config.embedding.backend.lower()
        if backend_str == "transformers":
            self._backend = EmbedderBackend.TRANSFORMERS
        else:
            # Default to Ollama
            self._backend = EmbedderBackend.OLLAMA

        # Initialize embedders (lazy loaded based on content type)
        self._text_embedder: BaseEmbedder | None = None
        self._code_embedder: BaseEmbedder | None = None
        self._multimodal_embedder: Any | None = None  # OpenCLIPEmbedder

    def _load_state(self) -> ProcessingState:
        """Load processing state from file."""
        state_path = self.config.processing.state_file
        if state_path.exists():
            try:
                data = json.loads(state_path.read_text())
                return ProcessingState(**data)
            except Exception:
                pass
        return ProcessingState()

    def _save_state(self) -> None:
        """Save processing state to file."""
        state_path = self.config.processing.state_file
        data = {
            "processed_files": self.state.processed_files,
            "last_run": self.state.last_run,
            "version": self.state.version,
        }
        state_path.write_text(json.dumps(data, indent=2))

    async def _get_text_embedder(self) -> BaseEmbedder:
        """Get or create text embedder based on configured backend."""
        if self._text_embedder is None:
            profile, backend = get_model_for_profile(
                "text", self.config.embedding.text_profile, self._backend
            )
            self._text_embedder = self._create_embedder(profile, backend)
        return self._text_embedder

    async def _get_code_embedder(self) -> BaseEmbedder:
        """Get or create code embedder based on configured backend."""
        if self._code_embedder is None:
            profile, backend = get_model_for_profile(
                "code", self.config.embedding.code_profile, self._backend
            )
            self._code_embedder = self._create_embedder(profile, backend)
        return self._code_embedder

    async def _get_multimodal_embedder(self) -> Any:
        """Get or create multimodal embedder (OpenCLIP for images)."""
        if self._multimodal_embedder is None:
            profile, _ = get_model_for_profile(
                "multimodal", self.config.embedding.multimodal_profile, EmbedderBackend.TRANSFORMERS
            )
            try:
                from ..embedders import get_openclip_embedder
                OpenCLIPEmbedder = get_openclip_embedder()
                self._multimodal_embedder = OpenCLIPEmbedder(
                    model_name=profile.open_clip_model,
                    pretrained=profile.open_clip_pretrained,
                    device=self.config.embedding.torch_device,
                )
            except ImportError:
                console.print("[yellow]OpenCLIP not available, skipping image visual embeddings[/yellow]")
                self._multimodal_embedder = None
        return self._multimodal_embedder

    def _create_embedder(self, profile: Any, backend: EmbedderBackend) -> BaseEmbedder:
        """Create embedder for the given profile and backend.

        Args:
            profile: ModelProfile with model configuration
            backend: Selected backend to use

        Returns:
            Configured embedder instance
        """
        if backend == EmbedderBackend.TRANSFORMERS:
            try:
                from ..embedders import get_transformers_embedder

                TransformersEmbedder = get_transformers_embedder()
                return TransformersEmbedder(
                    model=profile.huggingface_id,
                    device=self.config.embedding.torch_device,
                )
            except ImportError:
                console.print("[yellow]Transformers not available, falling back to Ollama[/yellow]")
                return OllamaEmbedder(
                    model=profile.ollama_model or profile.name,
                    host=self.config.embedding.ollama_host,
                )
        else:
            # Default: Ollama
            return OllamaEmbedder(
                model=profile.ollama_model or profile.name,
                host=self.config.embedding.ollama_host,
            )

    async def process(
        self,
        input_path: Path,
        content_type: str | None = None,
    ) -> dict[str, Any]:
        """Process files from input path.

        Args:
            input_path: File or directory to process
            content_type: Force content type ('auto', 'code', 'paper', 'markdown')

        Returns:
            Processing statistics
        """
        # Collect files to process
        files = self._collect_files(input_path)
        console.print(f"Found {len(files)} files to process")

        # Filter by incremental state
        if self.config.processing.incremental:
            files = [f for f in files if self.state.needs_processing(f)]
            console.print(f"Processing {len(files)} files (incremental mode)")

        # Process files (text and code)
        all_chunks: list[Chunk] = []
        errors = 0

        if files:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Processing files...", total=len(files))

                for file_path in files:
                    try:
                        result = await self._process_file(file_path, content_type)
                        if result.success:
                            all_chunks.extend(result.chunks)
                            self.state.mark_processed(file_path)
                        else:
                            errors += 1
                            if self.config.verbose:
                                for error in result.errors:
                                    console.print(f"[red]Error in {file_path}: {error}[/red]")
                    except Exception as e:
                        errors += 1
                        if self.config.verbose:
                            console.print(f"[red]Error processing {file_path}: {e}[/red]")

                    progress.update(task, advance=1)

            console.print(f"Created {len(all_chunks)} chunks from {len(files)} files")

        # Process images from papers
        image_chunks: list[ImageChunk] = []
        image_errors = 0

        console.print("Scanning for paper images...")
        paper_image_chunks, paper_errors = self.image_processor.get_all_image_chunks(
            input_path, verbose=self.config.verbose
        )
        image_chunks.extend(paper_image_chunks)
        image_errors += len(paper_errors)

        if image_chunks:
            console.print(f"Found {len(image_chunks)} images from papers")
        elif paper_errors:
            console.print(f"[yellow]Image processing errors: {len(paper_errors)}[/yellow]")

        # Initialize loader with input_root for portable paths
        input_root = input_path if input_path.is_dir() else input_path.parent
        loader = LanceDBLoader.from_config(self.config.database, input_root=input_root)

        # Embed and load text/code chunks
        if all_chunks:
            console.print(f"[cyan]Generating embeddings for {len(all_chunks)} chunks...[/cyan]")
            all_chunks = await self._embed_chunks(all_chunks)

            console.print("Loading text/code into LanceDB...")
            counts = await loader.load_chunks(all_chunks)
            console.print(f"[green]✓[/green] Loaded: text={counts['text_chunks']}, code={counts['code_chunks']}, unified={counts['unified_chunks']}")

        # Embed image chunks (dual embeddings)
        if image_chunks:
            console.print(f"[cyan]Generating embeddings for {len(image_chunks)} images...[/cyan]")
            image_chunks = await self._embed_image_chunks(image_chunks)

            console.print("Loading images into LanceDB...")
            image_counts = await loader.load_image_chunks(image_chunks)
            console.print(f"[green]✓[/green] Loaded: images={image_counts['image_chunks']}")

        # Save state
        from datetime import datetime
        self.state.last_run = datetime.now().isoformat()
        self._save_state()

        # Close embedders
        await self._close_embedders()

        return {
            "files_processed": len(files),
            "chunks_created": len(all_chunks),
            "images_processed": len(image_chunks),
            "errors": errors + image_errors,
        }

    def _collect_files(self, input_path: Path) -> list[Path]:
        """Collect all processable files from input path."""
        if input_path.is_file():
            if self.router.should_process(input_path):
                return [input_path]
            return []

        files = []
        for file_path in input_path.rglob("*"):
            if file_path.is_file() and self.router.should_process(file_path):
                files.append(file_path)

        return sorted(files)

    async def _process_file(
        self,
        file_path: Path,
        force_type: str | None = None,
    ) -> ProcessingResult:
        """Process a single file into chunks."""
        try:
            # Read file content
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            if not content.strip():
                return ProcessingResult(
                    source_file=str(file_path),
                    content_type=ContentType.TEXT,
                    chunks=[],
                    errors=["Empty file"],
                )

            # Detect content type
            content_type = self.detector.detect(file_path, force_type)

            # Get appropriate chunker
            chunker = self.chunker_factory.get_chunker_for_content_type(content_type)

            # Chunk content
            chunks = chunker.chunk(content, file_path)

            return ProcessingResult(
                source_file=str(file_path),
                content_type=content_type,
                chunks=chunks,
            )

        except Exception as e:
            return ProcessingResult(
                source_file=str(file_path),
                content_type=ContentType.TEXT,
                chunks=[],
                errors=[str(e)],
            )

    async def _embed_chunks(
        self,
        chunks: list[Chunk],
        progress: Progress | None = None,
    ) -> list[Chunk]:
        """Generate embeddings for chunks."""
        # Separate by type for different models
        text_chunks = [c for c in chunks if not c.source_type.value.startswith("code_")]
        code_chunks = [c for c in chunks if c.source_type.value.startswith("code_")]

        embedded_chunks = []

        # Embed text chunks
        if text_chunks:
            if self.config.verbose:
                console.print(f"Embedding {len(text_chunks)} text chunks...")

            embedder = await self._get_text_embedder()
            text_chunks = await self._embed_chunk_list(
                embedder, text_chunks, self.config.embedding.batch_size
            )
            embedded_chunks.extend(text_chunks)

        # Embed code chunks
        if code_chunks:
            if self.config.verbose:
                console.print(f"Embedding {len(code_chunks)} code chunks...")

            embedder = await self._get_code_embedder()
            code_chunks = await self._embed_chunk_list(
                embedder, code_chunks, self.config.embedding.batch_size
            )
            embedded_chunks.extend(code_chunks)

        return embedded_chunks

    async def _embed_chunk_list(
        self,
        embedder: BaseEmbedder,
        chunks: list[Chunk],
        batch_size: int,
    ) -> list[Chunk]:
        """Embed a list of chunks using the given embedder.

        Args:
            embedder: Embedder to use
            chunks: Chunks to embed
            batch_size: Batch size for embedding

        Returns:
            Chunks with embeddings set
        """
        texts = [c.content for c in chunks]
        embeddings = await embedder.embed_batch(texts, batch_size=batch_size)

        for chunk, embedding in zip(chunks, embeddings, strict=False):
            chunk.embedding = embedding

        return chunks

    async def _embed_image_chunks(
        self,
        image_chunks: list[ImageChunk],
    ) -> list[ImageChunk]:
        """Generate dual embeddings for image chunks.

        Each image gets:
        - text_embedding: From VLM description (via text embedder)
        - visual_embedding: From actual image (via CLIP/SigLIP)

        Args:
            image_chunks: ImageChunks to embed

        Returns:
            ImageChunks with both embeddings set
        """
        if not image_chunks:
            return image_chunks

        # Get text embeddings from VLM descriptions
        text_embedder = await self._get_text_embedder()
        texts = [chunk.searchable_text for chunk in image_chunks]

        if self.config.verbose:
            console.print(f"  Embedding {len(texts)} image descriptions...")

        text_embeddings = await text_embedder.embed_batch(
            texts, batch_size=self.config.embedding.batch_size
        )

        for chunk, embedding in zip(image_chunks, text_embeddings, strict=False):
            chunk.text_embedding = embedding

        # Get visual embeddings from images (if CLIP available)
        multimodal_embedder = await self._get_multimodal_embedder()

        if multimodal_embedder is not None:
            if self.config.verbose:
                console.print(f"  Embedding {len(image_chunks)} images with CLIP...")

            image_paths = [chunk.image_path for chunk in image_chunks]
            try:
                visual_embeddings = await multimodal_embedder.embed_images(image_paths)

                for chunk, embedding in zip(image_chunks, visual_embeddings, strict=False):
                    chunk.visual_embedding = embedding
            except Exception as e:
                console.print(f"[yellow]Visual embedding failed: {e}[/yellow]")
                # Set visual embeddings to None (or same as text)
                for chunk in image_chunks:
                    chunk.visual_embedding = chunk.text_embedding
        else:
            # No CLIP available - use text embedding for both
            console.print("[yellow]No multimodal embedder, using text embeddings for visual[/yellow]")
            for chunk in image_chunks:
                chunk.visual_embedding = chunk.text_embedding

        return image_chunks

    async def _close_embedders(self) -> None:
        """Close embedder connections."""
        if self._text_embedder:
            await self._text_embedder.close()
        if self._code_embedder:
            await self._code_embedder.close()
        if self._multimodal_embedder and hasattr(self._multimodal_embedder, 'close'):
            await self._multimodal_embedder.close()
