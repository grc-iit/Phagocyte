"""Image processor for extracting figures from papers."""

import json
from pathlib import Path

from ..types import ImageChunk, ImageProcessingResult


class ImageProcessor:
    """Process images from papers using figures.json metadata.

    Papers processed by the ingestor contain:
    - figures.json: VLM-generated descriptions for each figure
    - img/: Directory containing the actual image files

    This processor reads figures.json and creates ImageChunk objects
    that can be embedded using both text (VLM description) and visual
    (CLIP/SigLIP) embeddings.
    """

    # Classifications to skip (low-value figures)
    SKIP_CLASSIFICATIONS = {
        "logo",
        "icon",
        "decorative",
    }

    def __init__(self, skip_logos: bool = True):
        """Initialize the image processor.

        Args:
            skip_logos: Whether to skip figures classified as logos
        """
        self.skip_logos = skip_logos

    def process_paper_images(self, paper_dir: Path) -> ImageProcessingResult:
        """Process all images from a paper directory.

        Args:
            paper_dir: Path to the paper directory containing figures.json

        Returns:
            ImageProcessingResult with ImageChunks for each valid figure
        """
        errors: list[str] = []
        image_chunks: list[ImageChunk] = []

        figures_path = paper_dir / "figures.json"

        # Check if figures.json exists
        if not figures_path.exists():
            return ImageProcessingResult(
                source_paper=paper_dir.name,
                image_chunks=[],
                errors=[],  # Not an error if no figures
            )

        # Load figures.json
        try:
            figures_data = json.loads(figures_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            return ImageProcessingResult(
                source_paper=paper_dir.name,
                image_chunks=[],
                errors=[f"Failed to parse figures.json: {e}"],
            )
        except Exception as e:
            return ImageProcessingResult(
                source_paper=paper_dir.name,
                image_chunks=[],
                errors=[f"Failed to read figures.json: {e}"],
            )

        # Process each figure
        for fig_data in figures_data:
            try:
                chunk = ImageChunk.from_figure_json(fig_data, paper_dir)

                # Skip logos if configured
                if self.skip_logos and chunk.is_logo:
                    continue

                # Skip figures without useful content
                if not chunk.searchable_text.strip():
                    continue

                # Verify image file exists
                if not chunk.image_path.exists():
                    errors.append(
                        f"Image file not found: {chunk.image_path} (figure {chunk.figure_id})"
                    )
                    continue

                image_chunks.append(chunk)

            except Exception as e:
                fig_id = fig_data.get("figure_id", "unknown")
                errors.append(f"Failed to process figure {fig_id}: {e}")

        return ImageProcessingResult(
            source_paper=paper_dir.name,
            image_chunks=image_chunks,
            errors=errors,
        )

    def find_paper_directories(self, input_path: Path) -> list[Path]:
        """Find all paper directories containing figures.json.

        Args:
            input_path: Root input path to search

        Returns:
            List of paths to paper directories with figures.json
        """
        paper_dirs: list[Path] = []

        # Check if input_path itself is a paper directory
        if (input_path / "figures.json").exists():
            return [input_path]

        # Check for papers subdirectory
        papers_dir = input_path / "papers"
        if papers_dir.exists():
            for subdir in papers_dir.iterdir():
                if subdir.is_dir() and (subdir / "figures.json").exists():
                    paper_dirs.append(subdir)

        # Also check direct subdirectories
        for subdir in input_path.iterdir():
            if subdir.is_dir() and subdir.name != "papers":
                if (subdir / "figures.json").exists():
                    paper_dirs.append(subdir)

        return paper_dirs

    def process_all_papers(
        self, input_path: Path, verbose: bool = False
    ) -> list[ImageProcessingResult]:
        """Process images from all papers in input directory.

        Args:
            input_path: Root input path containing papers
            verbose: Whether to print progress

        Returns:
            List of ImageProcessingResult for each paper
        """
        results: list[ImageProcessingResult] = []
        paper_dirs = self.find_paper_directories(input_path)

        for paper_dir in paper_dirs:
            result = self.process_paper_images(paper_dir)
            results.append(result)

            if verbose and result.chunk_count > 0:
                print(f"  {paper_dir.name}: {result.chunk_count} figures")

        return results

    def get_all_image_chunks(
        self, input_path: Path, verbose: bool = False
    ) -> tuple[list[ImageChunk], list[str]]:
        """Get all image chunks from papers in input directory.

        Convenience method that flattens results from process_all_papers.

        Args:
            input_path: Root input path containing papers
            verbose: Whether to print progress

        Returns:
            Tuple of (all_chunks, all_errors)
        """
        all_chunks: list[ImageChunk] = []
        all_errors: list[str] = []

        results = self.process_all_papers(input_path, verbose=verbose)

        for result in results:
            all_chunks.extend(result.image_chunks)
            all_errors.extend(result.errors)

        return all_chunks, all_errors
