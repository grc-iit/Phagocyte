"""Unit tests for content detector and file filtering."""

import pytest
from pathlib import Path

from processor.core.detector import (
    ContentDetector,
    SKIP_PATTERNS,
    SKIP_EXTENSIONS,
    SKIP_DIRECTORIES,
)
from processor.types import ContentType


class TestSkipPatterns:
    """Test skip pattern constants."""

    def test_skip_patterns_defined(self) -> None:
        """Test that skip patterns are properly defined."""
        assert "_raw.md" in SKIP_PATTERNS
        assert ".bib" in SKIP_PATTERNS
        assert ".backup" in SKIP_PATTERNS

    def test_skip_extensions_defined(self) -> None:
        """Test that skip extensions are properly defined."""
        assert ".json" in SKIP_EXTENSIONS

    def test_skip_directories_defined(self) -> None:
        """Test that skip directories are properly defined."""
        assert ".git" in SKIP_DIRECTORIES
        assert "__pycache__" in SKIP_DIRECTORIES
        assert "node_modules" in SKIP_DIRECTORIES


class TestContentDetectorIsProcessable:
    """Test ContentDetector.is_processable() method."""

    @pytest.fixture
    def detector(self) -> ContentDetector:
        """Create detector instance."""
        return ContentDetector()

    # Files that SHOULD be processed
    @pytest.mark.parametrize("filename", [
        "document.md",
        "code.py",
        "script.sh",
        "main.cpp",
        "README.txt",
        "paper.rst",
    ])
    def test_processable_files(self, detector: ContentDetector, filename: str) -> None:
        """Test that valid files are marked as processable."""
        assert detector.is_processable(Path(filename)) is True

    # Files that should be SKIPPED - raw markdown
    @pytest.mark.parametrize("filename", [
        "document_raw.md",
        "paper_raw.md",
        "notes_raw.md",
    ])
    def test_skip_raw_markdown(self, detector: ContentDetector, filename: str) -> None:
        """Test that _raw.md files are skipped."""
        assert detector.is_processable(Path(filename)) is False

    # Files that should be SKIPPED - JSON
    @pytest.mark.parametrize("filename", [
        "figures.json",
        "code_blocks.json",
        "enrichments.json",
        "config.json",
    ])
    def test_skip_json_files(self, detector: ContentDetector, filename: str) -> None:
        """Test that JSON files are skipped."""
        assert detector.is_processable(Path(filename)) is False

    # Files that should be SKIPPED - other patterns
    @pytest.mark.parametrize("filename", [
        "refs.bib",
        "references.bib",
        "file.backup",
        "document.backup",
    ])
    def test_skip_other_patterns(self, detector: ContentDetector, filename: str) -> None:
        """Test that .bib and .backup files are skipped."""
        assert detector.is_processable(Path(filename)) is False

    # Files in skip directories should be SKIPPED
    @pytest.mark.parametrize("filepath", [
        ".git/config",
        ".git/HEAD",
        ".github/workflows/test.yml",
        "__pycache__/module.pyc",
        "node_modules/package/index.js",
        "venv/lib/python3.11/site.py",
    ])
    def test_skip_directories(self, detector: ContentDetector, filepath: str) -> None:
        """Test that files in skip directories are skipped."""
        assert detector.is_processable(Path(filepath)) is False

    # Hidden files should be SKIPPED
    @pytest.mark.parametrize("filename", [
        ".gitignore",
        ".env",
        ".hidden",
    ])
    def test_skip_hidden_files(self, detector: ContentDetector, filename: str) -> None:
        """Test that hidden files are skipped."""
        assert detector.is_processable(Path(filename)) is False

    # Binary files should be SKIPPED
    @pytest.mark.parametrize("filename", [
        "image.png",
        "photo.jpg",
        "doc.pdf",
        "archive.zip",
        "binary.exe",
    ])
    def test_skip_binary_files(self, detector: ContentDetector, filename: str) -> None:
        """Test that binary files are skipped."""
        assert detector.is_processable(Path(filename)) is False


class TestContentDetectorIsImageFile:
    """Test ContentDetector.is_image_file() method."""

    @pytest.fixture
    def detector(self) -> ContentDetector:
        """Create detector instance."""
        return ContentDetector()

    @pytest.mark.parametrize("filename,expected", [
        ("figure.png", True),
        ("photo.jpg", True),
        ("image.jpeg", True),
        ("chart.gif", True),
        ("diagram.bmp", True),
        ("icon.webp", True),
        ("document.pdf", False),
        ("code.py", False),
        ("data.json", False),
        ("image.svg", False),  # SVG is not in the list
    ])
    def test_is_image_file(
        self, detector: ContentDetector, filename: str, expected: bool
    ) -> None:
        """Test image file detection."""
        assert detector.is_image_file(Path(filename)) is expected


class TestContentDetectorDetect:
    """Test ContentDetector.detect() method."""

    @pytest.fixture
    def detector(self) -> ContentDetector:
        """Create detector instance."""
        return ContentDetector()

    def test_detect_python(self, detector: ContentDetector) -> None:
        """Test detecting Python files."""
        assert detector.detect(Path("script.py")) == ContentType.CODE_PYTHON
        assert detector.detect(Path("module.pyi")) == ContentType.CODE_PYTHON

    def test_detect_cpp(self, detector: ContentDetector) -> None:
        """Test detecting C++ files."""
        assert detector.detect(Path("main.cpp")) == ContentType.CODE_CPP
        assert detector.detect(Path("header.hpp")) == ContentType.CODE_CPP
        assert detector.detect(Path("source.cc")) == ContentType.CODE_CPP

    def test_detect_markdown(self, detector: ContentDetector) -> None:
        """Test detecting markdown files."""
        assert detector.detect(Path("README.md")) == ContentType.MARKDOWN
        assert detector.detect(Path("doc.markdown")) == ContentType.MARKDOWN

    def test_detect_from_directory(self, detector: ContentDetector) -> None:
        """Test detection from directory name."""
        # Papers directory -> PAPER type
        assert detector.detect(Path("papers/document.md")) == ContentType.PAPER

        # Codebases directory -> CODE type (specific determined by extension)
        result = detector.detect(Path("codebases/project/main.py"))
        assert result == ContentType.CODE_PYTHON

    def test_force_type(self, detector: ContentDetector) -> None:
        """Test forcing content type."""
        # Force paper type on any file
        assert detector.detect(Path("code.py"), force_type="paper") == ContentType.PAPER

        # Force code type
        result = detector.detect(Path("doc.md"), force_type="code")
        assert result == ContentType.CODE_OTHER

    def test_image_content_type_exists(self) -> None:
        """Test that IMAGE content type exists."""
        assert hasattr(ContentType, "IMAGE")
        assert ContentType.IMAGE.value == "image"
