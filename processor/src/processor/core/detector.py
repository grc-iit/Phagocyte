"""Content type detection based on directory structure and file extensions."""

from pathlib import Path

from ..types import ContentType

# Files to skip during processing
SKIP_PATTERNS: set[str] = {
    "_raw.md",      # Raw markdown versions (papers have clean versions)
    ".bib",         # BibTeX citation files
    ".backup",      # Backup files
}

# Extensions to skip (metadata files, not content)
SKIP_EXTENSIONS: set[str] = {
    ".json",        # JSON metadata files (figures.json, code_blocks.json, enrichments.json)
}

# Directories to skip entirely
SKIP_DIRECTORIES: set[str] = {
    ".git",
    ".github",
    "citations",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
}


class ContentDetector:
    """Detect content type from file path and directory structure."""

    # Map directory names to content types
    DIRECTORY_MAP: dict[str, str] = {
        "codebases": "code",
        "papers": "paper",
        "websites": "markdown",
        "books": "paper",
        "youtube": "markdown",
    }

    # Map file extensions to code types
    CODE_EXTENSIONS: dict[str, ContentType] = {
        ".cpp": ContentType.CODE_CPP,
        ".cc": ContentType.CODE_CPP,
        ".cxx": ContentType.CODE_CPP,
        ".c": ContentType.CODE_CPP,
        ".h": ContentType.CODE_CPP,
        ".hpp": ContentType.CODE_CPP,
        ".hxx": ContentType.CODE_CPP,
        ".py": ContentType.CODE_PYTHON,
        ".pyw": ContentType.CODE_PYTHON,
        ".pyi": ContentType.CODE_PYTHON,
        ".sh": ContentType.CODE_SHELL,
        ".bash": ContentType.CODE_SHELL,
        ".zsh": ContentType.CODE_SHELL,
        ".java": ContentType.CODE_JAVA,
        ".js": ContentType.CODE_JS,
        ".mjs": ContentType.CODE_JS,
        ".cjs": ContentType.CODE_JS,
        ".ts": ContentType.CODE_TS,
        ".tsx": ContentType.CODE_TS,
        ".jsx": ContentType.CODE_JS,
        ".go": ContentType.CODE_GO,
        ".rs": ContentType.CODE_RUST,
    }

    # Extensions that indicate markdown/text
    MARKDOWN_EXTENSIONS = {".md", ".markdown", ".rst", ".txt"}

    def __init__(self, directory_map: dict[str, str] | None = None):
        """Initialize detector with optional custom directory mapping."""
        if directory_map:
            self.DIRECTORY_MAP = {**self.DIRECTORY_MAP, **directory_map}

    def detect(self, file_path: Path, force_type: str | None = None) -> ContentType:
        """Detect content type for a file.

        Args:
            file_path: Path to the file
            force_type: Force a specific type (auto, code, paper, markdown)

        Returns:
            Detected ContentType
        """
        # Handle forced type
        if force_type and force_type != "auto":
            return self._type_from_string(force_type, file_path)

        # Check directory structure first
        dir_type = self._detect_from_directory(file_path)
        if dir_type:
            if dir_type == "code":
                return self._detect_code_type(file_path)
            elif dir_type == "paper":
                return ContentType.PAPER
            elif dir_type == "markdown":
                return ContentType.MARKDOWN

        # Fallback to extension-based detection
        return self._detect_from_extension(file_path)

    def _detect_from_directory(self, file_path: Path) -> str | None:
        """Detect content type from directory name."""
        parts = file_path.parts

        for part in parts:
            part_lower = part.lower()
            if part_lower in self.DIRECTORY_MAP:
                return self.DIRECTORY_MAP[part_lower]

        return None

    def _detect_from_extension(self, file_path: Path) -> ContentType:
        """Detect content type from file extension."""
        ext = file_path.suffix.lower()

        # Check for code files
        if ext in self.CODE_EXTENSIONS:
            return self.CODE_EXTENSIONS[ext]

        # Check for markdown/text
        if ext in self.MARKDOWN_EXTENSIONS:
            return ContentType.MARKDOWN

        # Default to text
        return ContentType.TEXT

    def _detect_code_type(self, file_path: Path) -> ContentType:
        """Detect specific code type from extension."""
        ext = file_path.suffix.lower()
        return self.CODE_EXTENSIONS.get(ext, ContentType.CODE_OTHER)

    def _type_from_string(self, type_str: str, file_path: Path) -> ContentType:
        """Convert string type to ContentType."""
        type_map = {
            "code": self._detect_code_type(file_path),
            "paper": ContentType.PAPER,
            "markdown": ContentType.MARKDOWN,
            "text": ContentType.TEXT,
        }
        return type_map.get(type_str, ContentType.TEXT)

    def is_processable(self, file_path: Path) -> bool:
        """Check if file should be processed.

        Skips:
        - Hidden files (starting with .)
        - Files in skip directories (.git, __pycache__, etc.)
        - Files matching skip patterns (_raw.md, .bib, .backup)
        - Files with skip extensions (.json)
        - Binary files (images, PDFs, archives, etc.)
        """
        # Skip hidden files
        if file_path.name.startswith("."):
            return False

        # Skip files in skip directories
        for part in file_path.parts:
            if part in SKIP_DIRECTORIES:
                return False

        # Skip files matching skip patterns (e.g., _raw.md)
        filename = file_path.name
        for pattern in SKIP_PATTERNS:
            if filename.endswith(pattern):
                return False

        # Skip files with skip extensions (.json)
        if file_path.suffix.lower() in SKIP_EXTENSIONS:
            return False

        # Skip non-text files (binary)
        binary_extensions = {
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
            ".zip", ".tar", ".gz", ".rar", ".7z",
            ".exe", ".dll", ".so", ".dylib",
            ".pyc", ".pyo", ".class", ".o", ".a",
            ".mp3", ".mp4", ".wav", ".avi", ".mov",
        }

        if file_path.suffix.lower() in binary_extensions:
            return False

        return True

    def is_image_file(self, file_path: Path) -> bool:
        """Check if file is a processable image (for multimodal embedding)."""
        image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
        return file_path.suffix.lower() in image_extensions
