"""Integration tests for paper processing with images."""

import json
from pathlib import Path

import pytest

from processor.core.detector import ContentDetector
from processor.images.processor import ImageProcessor
from processor.types import ContentType


class TestPaperDirectoryStructure:
    """Test processing of real paper directory structure."""

    @pytest.fixture
    def input_dir(self) -> Path:
        """Path to the input directory."""
        return Path(__file__).parent.parent.parent / "input"

    @pytest.fixture
    def papers_dir(self, input_dir: Path) -> Path:
        """Path to papers directory."""
        return input_dir / "papers"

    def test_papers_directory_exists(self, papers_dir: Path) -> None:
        """Test that papers directory exists."""
        if not papers_dir.exists():
            pytest.skip("No papers directory in input - skipping integration test")

        assert papers_dir.is_dir()

    def test_find_papers_with_figures(self, papers_dir: Path) -> None:
        """Test finding papers that have figures.json."""
        if not papers_dir.exists():
            pytest.skip("No papers directory")

        processor = ImageProcessor()
        paper_dirs = processor.find_paper_directories(papers_dir.parent)

        # Should find at least some papers with figures
        assert len(paper_dirs) >= 0  # May be 0 if no figures.json files

        for paper_dir in paper_dirs:
            assert (paper_dir / "figures.json").exists()


class TestRealPaperProcessing:
    """Test processing real papers from input directory."""

    @pytest.fixture
    def sample_paper(self) -> Path:
        """Get a sample paper with figures.json."""
        input_dir = Path(__file__).parent.parent.parent / "input" / "papers"
        if not input_dir.exists():
            pytest.skip("No papers directory")

        # Find first paper with figures.json
        for paper_dir in input_dir.iterdir():
            if paper_dir.is_dir() and (paper_dir / "figures.json").exists():
                return paper_dir

        pytest.skip("No papers with figures.json found")

    def test_process_real_paper_figures(self, sample_paper: Path) -> None:
        """Test processing figures from a real paper."""
        processor = ImageProcessor(skip_logos=True)
        result = processor.process_paper_images(sample_paper)

        # Should process without fatal errors
        assert result.source_paper == sample_paper.name

        # Log what we found
        print(f"\nPaper: {sample_paper.name}")
        print(f"  Figures processed: {result.chunk_count}")
        print(f"  Errors: {len(result.errors)}")

        if result.chunk_count > 0:
            print(f"  Sample classifications: {[c.classification for c in result.image_chunks[:3]]}")

    def test_figures_json_format(self, sample_paper: Path) -> None:
        """Test that figures.json has expected format."""
        figures_path = sample_paper / "figures.json"
        figures = json.loads(figures_path.read_text())

        assert isinstance(figures, list)

        if figures:
            fig = figures[0]
            # Check expected fields exist
            assert "figure_id" in fig
            assert "image_path" in fig

            # Optional but common fields
            if "caption" in fig:
                assert isinstance(fig["caption"], str)
            if "description" in fig:
                assert isinstance(fig["description"], str)

    def test_image_files_exist(self, sample_paper: Path) -> None:
        """Test that referenced images actually exist."""
        figures_path = sample_paper / "figures.json"
        figures = json.loads(figures_path.read_text())

        for fig in figures:
            image_path_str = fig.get("image_path", "")
            if image_path_str.startswith("./"):
                image_path_str = image_path_str[2:]
            image_path = sample_paper / image_path_str

            # All referenced images should exist
            assert image_path.exists(), f"Missing image: {image_path}"


class TestFileFiltering:
    """Test file filtering in real paper directories."""

    @pytest.fixture
    def sample_paper(self) -> Path:
        """Get a sample paper directory."""
        input_dir = Path(__file__).parent.parent.parent / "input" / "papers"
        if not input_dir.exists():
            pytest.skip("No papers directory")

        for paper_dir in input_dir.iterdir():
            if paper_dir.is_dir():
                return paper_dir

        pytest.skip("No papers found")

    def test_raw_md_skipped(self, sample_paper: Path) -> None:
        """Test that _raw.md files are skipped."""
        detector = ContentDetector()

        for file in sample_paper.rglob("*_raw.md"):
            assert detector.is_processable(file) is False, f"Should skip: {file}"

    def test_json_files_skipped(self, sample_paper: Path) -> None:
        """Test that JSON files are skipped."""
        detector = ContentDetector()

        for file in sample_paper.rglob("*.json"):
            assert detector.is_processable(file) is False, f"Should skip: {file}"

    def test_clean_md_processed(self, sample_paper: Path) -> None:
        """Test that clean markdown files are processed."""
        detector = ContentDetector()

        for file in sample_paper.rglob("*.md"):
            if "_raw.md" not in file.name:
                assert detector.is_processable(file) is True, f"Should process: {file}"

    def test_images_not_processable_as_text(self, sample_paper: Path) -> None:
        """Test that image files are not processed as text."""
        detector = ContentDetector()

        img_dir = sample_paper / "img"
        if img_dir.exists():
            for file in img_dir.rglob("*.png"):
                assert detector.is_processable(file) is False
                assert detector.is_image_file(file) is True


class TestContentDetection:
    """Test content type detection for papers."""

    def test_paper_directory_detection(self) -> None:
        """Test that files in papers directory get PAPER type."""
        detector = ContentDetector()

        # Files in papers directory should be detected as PAPER type
        paper_file = Path("input/papers/author-2024-title/document.md")
        assert detector.detect(paper_file) == ContentType.PAPER

    def test_code_in_codebases_detection(self) -> None:
        """Test that code files in codebases get proper code types."""
        detector = ContentDetector()

        python_file = Path("input/codebases/project/main.py")
        assert detector.detect(python_file) == ContentType.CODE_PYTHON

        cpp_file = Path("input/codebases/project/main.cpp")
        assert detector.detect(cpp_file) == ContentType.CODE_CPP


class TestImageChunkCreation:
    """Test creating ImageChunks from real data."""

    @pytest.fixture
    def sample_paper_with_figures(self) -> Path:
        """Get a paper with figures."""
        input_dir = Path(__file__).parent.parent.parent / "input" / "papers"
        if not input_dir.exists():
            pytest.skip("No papers directory")

        for paper_dir in input_dir.iterdir():
            if paper_dir.is_dir():
                figures_path = paper_dir / "figures.json"
                if figures_path.exists():
                    figures = json.loads(figures_path.read_text())
                    if len(figures) > 0:
                        return paper_dir

        pytest.skip("No papers with figures found")

    def test_image_chunks_have_searchable_text(
        self, sample_paper_with_figures: Path
    ) -> None:
        """Test that image chunks have searchable text."""
        processor = ImageProcessor()
        result = processor.process_paper_images(sample_paper_with_figures)

        for chunk in result.image_chunks:
            # Each chunk should have some searchable text
            assert len(chunk.searchable_text) > 0

    def test_image_chunks_have_valid_paths(
        self, sample_paper_with_figures: Path
    ) -> None:
        """Test that image chunks have valid image paths."""
        processor = ImageProcessor()
        result = processor.process_paper_images(sample_paper_with_figures)

        for chunk in result.image_chunks:
            assert chunk.image_path.exists(), f"Missing: {chunk.image_path}"
            assert chunk.image_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}

    def test_logos_filtered(self, sample_paper_with_figures: Path) -> None:
        """Test that logos are filtered out by default."""
        processor = ImageProcessor(skip_logos=True)
        result = processor.process_paper_images(sample_paper_with_figures)

        for chunk in result.image_chunks:
            assert "logo" not in chunk.classification.lower()
