"""Base chunker class that all content chunkers inherit from."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..types import Chunk, ContentType


class BaseChunker(ABC):
    """Abstract base class for all content chunkers.

    All chunkers must implement:
    - chunk(): Split content into chunks
    - supports(): Check if this chunker handles the given content type
    """

    content_types: list[ContentType] = []

    # Default chunk size parameters (characters, will be converted to ~tokens)
    default_chunk_size: int = 4000  # ~1000 tokens
    default_chunk_overlap: int = 400  # ~100 tokens

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        """Initialize chunker with size parameters.

        Args:
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size or self.default_chunk_size
        self.chunk_overlap = chunk_overlap or self.default_chunk_overlap

    @abstractmethod
    def chunk(
        self,
        content: str,
        source_file: Path,
        metadata: dict[str, Any] | None = None,
    ) -> list[Chunk]:
        """Split content into chunks.

        Args:
            content: Text content to chunk
            source_file: Original file path for metadata
            metadata: Additional metadata to attach

        Returns:
            List of Chunk objects
        """
        pass

    @abstractmethod
    def supports(self, content_type: ContentType) -> bool:
        """Check if this chunker can handle the given content type.

        Args:
            content_type: The content type to check

        Returns:
            True if this chunker can handle the content type
        """
        pass

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text (rough: 4 chars per token)."""
        return len(text) // 4

    @classmethod
    def get_name(cls) -> str:
        """Get the name of this chunker."""
        return cls.__name__.replace("Adapter", "").replace("Chunker", "").lower()
