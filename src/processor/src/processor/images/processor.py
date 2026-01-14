"""Image processor for extracting figures from papers and standalone images."""

import json
import re
from pathlib import Path

from ..types import ImageChunk, ImageProcessingResult


# Supported image extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


class ImageProcessor:
    """Process images from papers using figures.json metadata OR standalone images.

    Papers processed by the ingestor contain:
    - figures.json: VLM-generated descriptions for each figure
    - img/: Directory containing the actual image files

    For standalone images (no figures.json):
    - Scans recursively for image files
    - Creates ImageChunks with filename-derived descriptions
    - Can be embedded using visual (CLIP/SigLIP) embeddings

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

    def __init__(self, skip_logos: bool = True, process_standalone: bool = True):
        """Initialize the image processor.

        Args:
            skip_logos: Whether to skip figures classified as logos
            process_standalone: Whether to process standalone images without figures.json
        """
        self.skip_logos = skip_logos
        self.process_standalone = process_standalone

    def process_paper_images(self, paper_dir: Path) -> ImageProcessingResult:
        """Process all images from a paper directory.

        Args:
            paper_dir: Path to the paper directory containing figures.json or img/

        Returns:
            ImageProcessingResult with ImageChunks for each valid figure
        """
        errors: list[str] = []
        image_chunks: list[ImageChunk] = []

        figures_path = paper_dir / "figures.json"

        # Try figures.json first (preferred - has VLM descriptions)
        if figures_path.exists():
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

        # Fallback: process standalone images from img/ folder
        elif self.process_standalone:
            img_dir = paper_dir / "img"
            if img_dir.exists():
                standalone_chunks, standalone_errors = self._process_standalone_images(
                    img_dir, paper_dir.name
                )
                image_chunks.extend(standalone_chunks)
                errors.extend(standalone_errors)

        return ImageProcessingResult(
            source_paper=paper_dir.name,
            image_chunks=image_chunks,
            errors=errors,
        )

    def find_paper_directories(self, input_path: Path) -> list[Path]:
        """Find all paper directories containing figures.json or img/ folders.

        Args:
            input_path: Root input path to search

        Returns:
            List of paths to paper directories with figures.json or img/
        """
        paper_dirs: list[Path] = []

        # Check if input_path itself is a paper directory
        if (input_path / "figures.json").exists() or (input_path / "img").exists():
            return [input_path]

        # Check for papers or pdfs subdirectory
        for subdir_name in ["papers", "pdfs"]:
            subdir = input_path / subdir_name
            if subdir.exists():
                for item in subdir.iterdir():
                    if item.is_dir():
                        if (item / "figures.json").exists() or (item / "img").exists():
                            paper_dirs.append(item)

        # Also check direct subdirectories
        for subdir in input_path.iterdir():
            if subdir.is_dir() and subdir.name not in ["papers", "pdfs"]:
                if (subdir / "figures.json").exists() or (subdir / "img").exists():
                    paper_dirs.append(subdir)

        return paper_dirs

    def find_all_standalone_images(self, input_path: Path) -> list[Path]:
        """Recursively find all image files in a directory tree.

        Args:
            input_path: Root path to search

        Returns:
            List of paths to image files
        """
        image_files: list[Path] = []

        for file_path in input_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                image_files.append(file_path)

        return sorted(image_files)

    def _process_standalone_images(
        self, img_dir: Path, source_name: str
    ) -> tuple[list[ImageChunk], list[str]]:
        """Process standalone images from an img/ directory.

        Args:
            img_dir: Path to the img/ directory
            source_name: Name of the source (paper/folder name)

        Returns:
            Tuple of (image_chunks, errors)
        """
        image_chunks: list[ImageChunk] = []
        errors: list[str] = []

        image_files = sorted(
            f for f in img_dir.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
        )

        for idx, img_path in enumerate(image_files, 1):
            try:
                chunk = ImageChunk.from_standalone_image(
                    image_path=img_path,
                    source_name=source_name,
                    figure_id=idx,
                )
                image_chunks.append(chunk)
            except Exception as e:
                errors.append(f"Failed to process image {img_path.name}: {e}")

        return image_chunks, errors

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
