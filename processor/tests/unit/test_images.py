"""Unit tests for image processing module."""

import json
import pytest
from pathlib import Path
from typing import Any

from processor.types import ImageChunk, ImageProcessingResult, ContentType
from processor.images.processor import ImageProcessor


class TestImageChunk:
    """Test ImageChunk dataclass."""

    @pytest.fixture
    def sample_figure_data(self) -> dict[str, Any]:
        """Sample figure data from figures.json."""
        return {
            "figure_id": 3,
            "caption": "Figure 1: System architecture diagram",
            "classification": "flowchart (0.95)",
            "description": "The image shows a flowchart illustrating the system architecture with multiple components.",
            "page": 5,
            "image_path": "./img/figure3.png",
        }

    @pytest.fixture
    def paper_dir(self, tmp_path: Path) -> Path:
        """Create a temporary paper directory."""
        paper = tmp_path / "author-2024-paper-abc123"
        paper.mkdir()
        img_dir = paper / "img"
        img_dir.mkdir()
        # Create a dummy image file
        (img_dir / "figure3.png").write_bytes(b"fake image data")
        return paper

    def test_from_figure_json(
        self, sample_figure_data: dict[str, Any], paper_dir: Path
    ) -> None:
        """Test creating ImageChunk from figures.json entry."""
        chunk = ImageChunk.from_figure_json(sample_figure_data, paper_dir)

        assert chunk.figure_id == 3
        assert chunk.caption == "Figure 1: System architecture diagram"
        assert "flowchart illustrating" in chunk.vlm_description
        assert chunk.classification == "flowchart (0.95)"
        assert chunk.page == 5
        assert chunk.source_paper == paper_dir.name
        assert chunk.image_path == paper_dir / "img" / "figure3.png"

    def test_id_generation(
        self, sample_figure_data: dict[str, Any], paper_dir: Path
    ) -> None:
        """Test that ID is properly generated."""
        chunk = ImageChunk.from_figure_json(sample_figure_data, paper_dir)

        assert chunk.id == f"{paper_dir.name}:fig3"

    def test_searchable_text(
        self, sample_figure_data: dict[str, Any], paper_dir: Path
    ) -> None:
        """Test searchable_text property combines caption and description."""
        chunk = ImageChunk.from_figure_json(sample_figure_data, paper_dir)

        text = chunk.searchable_text
        assert "Figure 1: System architecture diagram" in text
        assert "flowchart illustrating" in text
        # Caption and description separated by double newline
        assert "\n\n" in text

    def test_searchable_text_empty_caption(self, paper_dir: Path) -> None:
        """Test searchable_text when caption is empty."""
        data = {
            "figure_id": 1,
            "caption": "",
            "description": "A diagram showing data flow.",
            "classification": "diagram",
            "page": 1,
            "image_path": "./img/figure1.png",
        }
        (paper_dir / "img" / "figure1.png").write_bytes(b"fake")

        chunk = ImageChunk.from_figure_json(data, paper_dir)

        assert chunk.searchable_text == "A diagram showing data flow."

    def test_is_logo_true(self, paper_dir: Path) -> None:
        """Test is_logo property returns True for logos."""
        data = {
            "figure_id": 1,
            "caption": "Company Logo",
            "description": "The company logo.",
            "classification": "logo (0.98)",
            "page": 1,
            "image_path": "./img/logo.png",
        }
        (paper_dir / "img" / "logo.png").write_bytes(b"fake")

        chunk = ImageChunk.from_figure_json(data, paper_dir)

        assert chunk.is_logo is True

    def test_is_logo_false(
        self, sample_figure_data: dict[str, Any], paper_dir: Path
    ) -> None:
        """Test is_logo property returns False for non-logos."""
        chunk = ImageChunk.from_figure_json(sample_figure_data, paper_dir)

        assert chunk.is_logo is False

    def test_embeddings_initially_none(
        self, sample_figure_data: dict[str, Any], paper_dir: Path
    ) -> None:
        """Test that embeddings are initially None."""
        chunk = ImageChunk.from_figure_json(sample_figure_data, paper_dir)

        assert chunk.text_embedding is None
        assert chunk.visual_embedding is None

    def test_image_path_relative_handling(self, paper_dir: Path) -> None:
        """Test that relative image paths are handled correctly."""
        # Test with ./ prefix
        data1 = {
            "figure_id": 1,
            "caption": "Test",
            "description": "Test",
            "classification": "other",
            "page": 1,
            "image_path": "./img/test.png",
        }
        (paper_dir / "img" / "test.png").write_bytes(b"fake")

        chunk = ImageChunk.from_figure_json(data1, paper_dir)
        assert chunk.image_path == paper_dir / "img" / "test.png"


class TestImageProcessingResult:
    """Test ImageProcessingResult dataclass."""

    def test_chunk_count(self) -> None:
        """Test chunk_count property."""
        chunks = [
            ImageChunk(
                id="test:fig1", figure_id=1, caption="", vlm_description="",
                classification="", page=1, image_path=Path("test.png"),
                source_paper="test"
            ),
            ImageChunk(
                id="test:fig2", figure_id=2, caption="", vlm_description="",
                classification="", page=2, image_path=Path("test2.png"),
                source_paper="test"
            ),
        ]
        result = ImageProcessingResult(source_paper="test", image_chunks=chunks)

        assert result.chunk_count == 2

    def test_has_errors(self) -> None:
        """Test has_errors property."""
        result_no_errors = ImageProcessingResult(
            source_paper="test", image_chunks=[], errors=[]
        )
        assert result_no_errors.has_errors is False

        result_with_errors = ImageProcessingResult(
            source_paper="test", image_chunks=[], errors=["Some error"]
        )
        assert result_with_errors.has_errors is True

    def test_success(self) -> None:
        """Test success property."""
        result_success = ImageProcessingResult(
            source_paper="test", image_chunks=[], errors=[]
        )
        assert result_success.success is True

        result_failure = ImageProcessingResult(
            source_paper="test", image_chunks=[], errors=["Error"]
        )
        assert result_failure.success is False


class TestImageProcessor:
    """Test ImageProcessor class."""

    @pytest.fixture
    def processor(self) -> ImageProcessor:
        """Create ImageProcessor instance."""
        return ImageProcessor(skip_logos=True)

    @pytest.fixture
    def paper_with_figures(self, tmp_path: Path) -> Path:
        """Create a paper directory with figures.json and images."""
        paper = tmp_path / "devarajan-2024-dftracer-8fcb"
        paper.mkdir()
        img_dir = paper / "img"
        img_dir.mkdir()

        # Create figures.json
        figures = [
            {
                "figure_id": 1,
                "caption": "Figure 1: System overview",
                "classification": "flowchart (0.95)",
                "description": "A flowchart showing the system overview.",
                "page": 1,
                "image_path": "./img/figure1.png",
            },
            {
                "figure_id": 2,
                "caption": "Figure 2: Performance results",
                "classification": "bar_chart (0.90)",
                "description": "Bar chart comparing performance metrics.",
                "page": 3,
                "image_path": "./img/figure2.png",
            },
            {
                "figure_id": 3,
                "caption": "Company Logo",
                "classification": "logo (0.99)",
                "description": "The company logo.",
                "page": 1,
                "image_path": "./img/logo.png",
            },
        ]
        (paper / "figures.json").write_text(json.dumps(figures))

        # Create image files
        (img_dir / "figure1.png").write_bytes(b"fake image 1")
        (img_dir / "figure2.png").write_bytes(b"fake image 2")
        (img_dir / "logo.png").write_bytes(b"fake logo")

        return paper

    def test_process_paper_images(
        self, processor: ImageProcessor, paper_with_figures: Path
    ) -> None:
        """Test processing images from a paper directory."""
        result = processor.process_paper_images(paper_with_figures)

        assert result.source_paper == paper_with_figures.name
        # Should have 2 figures (logo skipped)
        assert result.chunk_count == 2
        assert result.has_errors is False

        # Check figure IDs
        figure_ids = {c.figure_id for c in result.image_chunks}
        assert figure_ids == {1, 2}  # Logo (id=3) should be skipped

    def test_process_paper_no_figures_json(
        self, processor: ImageProcessor, tmp_path: Path
    ) -> None:
        """Test processing paper without figures.json."""
        paper = tmp_path / "no-figures"
        paper.mkdir()

        result = processor.process_paper_images(paper)

        assert result.chunk_count == 0
        assert result.has_errors is False

    def test_process_paper_invalid_json(
        self, processor: ImageProcessor, tmp_path: Path
    ) -> None:
        """Test processing paper with invalid figures.json."""
        paper = tmp_path / "invalid-json"
        paper.mkdir()
        (paper / "figures.json").write_text("{ invalid json }")

        result = processor.process_paper_images(paper)

        assert result.chunk_count == 0
        assert result.has_errors is True
        assert "parse" in result.errors[0].lower()

    def test_process_paper_missing_image(
        self, processor: ImageProcessor, tmp_path: Path
    ) -> None:
        """Test processing paper with missing image file."""
        paper = tmp_path / "missing-image"
        paper.mkdir()
        (paper / "img").mkdir()

        figures = [{
            "figure_id": 1,
            "caption": "Test",
            "classification": "chart",
            "description": "Description",
            "page": 1,
            "image_path": "./img/nonexistent.png",
        }]
        (paper / "figures.json").write_text(json.dumps(figures))

        result = processor.process_paper_images(paper)

        assert result.chunk_count == 0
        assert result.has_errors is True
        assert "not found" in result.errors[0].lower()

    def test_skip_logos_enabled(
        self, paper_with_figures: Path
    ) -> None:
        """Test that logos are skipped when skip_logos=True."""
        processor = ImageProcessor(skip_logos=True)
        result = processor.process_paper_images(paper_with_figures)

        classifications = [c.classification for c in result.image_chunks]
        assert not any("logo" in c.lower() for c in classifications)

    def test_skip_logos_disabled(
        self, paper_with_figures: Path
    ) -> None:
        """Test that logos are included when skip_logos=False."""
        processor = ImageProcessor(skip_logos=False)
        result = processor.process_paper_images(paper_with_figures)

        # Should have all 3 figures including logo
        assert result.chunk_count == 3

    def test_find_paper_directories(
        self, processor: ImageProcessor, tmp_path: Path
    ) -> None:
        """Test finding paper directories with figures.json."""
        # Create input structure
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        papers_dir = input_dir / "papers"
        papers_dir.mkdir()

        # Create two papers with figures.json
        paper1 = papers_dir / "paper1"
        paper1.mkdir()
        (paper1 / "figures.json").write_text("[]")

        paper2 = papers_dir / "paper2"
        paper2.mkdir()
        (paper2 / "figures.json").write_text("[]")

        # Create one paper without figures.json
        paper3 = papers_dir / "paper3"
        paper3.mkdir()

        found = processor.find_paper_directories(input_dir)

        assert len(found) == 2
        names = {p.name for p in found}
        assert names == {"paper1", "paper2"}

    def test_get_all_image_chunks(
        self, processor: ImageProcessor, tmp_path: Path
    ) -> None:
        """Test getting all image chunks from multiple papers."""
        input_dir = tmp_path / "input"
        papers_dir = input_dir / "papers"
        papers_dir.mkdir(parents=True)

        # Create paper 1
        paper1 = papers_dir / "paper1"
        paper1.mkdir()
        (paper1 / "img").mkdir()
        (paper1 / "figures.json").write_text(json.dumps([
            {
                "figure_id": 1, "caption": "Fig 1", "classification": "chart",
                "description": "Chart 1", "page": 1, "image_path": "./img/f1.png"
            }
        ]))
        (paper1 / "img" / "f1.png").write_bytes(b"img1")

        # Create paper 2
        paper2 = papers_dir / "paper2"
        paper2.mkdir()
        (paper2 / "img").mkdir()
        (paper2 / "figures.json").write_text(json.dumps([
            {
                "figure_id": 1, "caption": "Fig 1", "classification": "diagram",
                "description": "Diagram 1", "page": 1, "image_path": "./img/f1.png"
            },
            {
                "figure_id": 2, "caption": "Fig 2", "classification": "graph",
                "description": "Graph 1", "page": 2, "image_path": "./img/f2.png"
            }
        ]))
        (paper2 / "img" / "f1.png").write_bytes(b"img1")
        (paper2 / "img" / "f2.png").write_bytes(b"img2")

        chunks, errors = processor.get_all_image_chunks(input_dir)

        assert len(chunks) == 3  # 1 from paper1 + 2 from paper2
        assert len(errors) == 0
