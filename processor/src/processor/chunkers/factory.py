"""Factory for creating appropriate chunkers based on content type."""


from ..config import ChunkingConfig
from ..types import ContentType
from .adapters import LlamaIndexCodeAdapter, LlamaIndexMarkdownAdapter
from .base import BaseChunker


class ChunkerFactory:
    """Factory to create chunkers based on content type.

    Uses LlamaIndex-based chunkers:
    - Code: LlamaIndexCodeAdapter with tree-sitter AST parsing
    - Everything else: LlamaIndexMarkdownAdapter with header-aware parsing
    """

    def __init__(self, config: ChunkingConfig | None = None):
        """Initialize factory with optional chunking config."""
        self.config = config or ChunkingConfig()
        self._chunkers: dict[str, BaseChunker] = {}

    def get_chunker(self, chunker_type: str) -> BaseChunker:
        """Get or create a chunker for the given type.

        Args:
            chunker_type: Type of chunker ('code', 'paper', 'markdown', 'text')

        Returns:
            Appropriate chunker instance
        """
        if chunker_type not in self._chunkers:
            self._chunkers[chunker_type] = self._create_chunker(chunker_type)

        return self._chunkers[chunker_type]

    def get_chunker_for_content_type(self, content_type: ContentType) -> BaseChunker:
        """Get chunker for a specific ContentType.

        Args:
            content_type: The ContentType to get chunker for

        Returns:
            Appropriate chunker instance
        """
        chunker_type = self._content_type_to_chunker_type(content_type)
        return self.get_chunker(chunker_type)

    def _create_chunker(self, chunker_type: str) -> BaseChunker:
        """Create a new chunker instance.

        Note: We use structure-aware chunking which provides semantic boundaries:
        - Code: tree-sitter AST (function/class boundaries)
        - Text: header-aware parsing (section boundaries)
        """
        if chunker_type == "code":
            # AST-based code chunking via tree-sitter
            return LlamaIndexCodeAdapter(
                chunk_size=self.config.code_chunk_size * 4,  # Convert tokens to chars
            )
        else:
            # Header-aware markdown chunking for all text content
            # (papers, markdown, websites, books, youtube, text)
            return LlamaIndexMarkdownAdapter(
                chunk_size=self.config.markdown_chunk_size * 4,
            )

    def _content_type_to_chunker_type(self, content_type: ContentType) -> str:
        """Map ContentType to chunker type string."""
        if content_type.value.startswith("code_"):
            return "code"
        else:
            # All non-code content uses markdown chunker
            return "markdown"
