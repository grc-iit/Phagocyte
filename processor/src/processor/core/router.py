"""Content routing to appropriate chunkers."""

from pathlib import Path

from ..types import ContentType
from .detector import ContentDetector


class ContentRouter:
    """Route content to appropriate chunkers based on type."""

    def __init__(self, detector: ContentDetector | None = None):
        """Initialize router with optional custom detector."""
        self.detector = detector or ContentDetector()

    def get_chunker_type(self, file_path: Path, force_type: str | None = None) -> str:
        """Get the chunker type for a file.

        Args:
            file_path: Path to the file
            force_type: Force a specific content type

        Returns:
            Chunker type string: 'code', 'paper', 'markdown'
        """
        content_type = self.detector.detect(file_path, force_type)

        # Map content types to chunker types
        if content_type.value.startswith("code_"):
            return "code"
        elif content_type == ContentType.PAPER:
            return "paper"
        elif content_type in (ContentType.MARKDOWN, ContentType.WEBSITE, ContentType.BOOK):
            return "markdown"
        else:
            return "text"

    def should_process(self, file_path: Path) -> bool:
        """Check if a file should be processed."""
        return self.detector.is_processable(file_path)
