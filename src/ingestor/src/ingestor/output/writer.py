"""Output writer for extraction results."""

import json
import re
from pathlib import Path

import aiofiles

from ..images.processor import ImageProcessor
from ..types import ExtractionResult, IngestConfig


class OutputWriter:
    """Write extraction results to disk.

    Creates output structure:
    output/
    ├── document_name/
    │   ├── document_name.md
    │   ├── img/
    │   │   ├── document_name_img_001.png
    │   │   └── ...
    │   └── metadata.json (optional)
    """

    def __init__(self, config: IngestConfig | None = None):
        """Initialize the writer.

        Args:
            config: Configuration options
        """
        self.config = config or IngestConfig()
        self.image_processor = ImageProcessor(config)

    async def write(self, result: ExtractionResult) -> Path:
        """Write an extraction result to disk.

        Args:
            result: Extraction result to write

        Returns:
            Path to the output directory
        """
        # Determine output directory name
        if result.source:
            name = self._clean_name(result.source)
        elif result.title:
            name = self._clean_name(result.title)
        else:
            name = "output"

        output_dir = self.config.output_dir / name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Process and write images
        original_images = result.images.copy() if result.images else []
        if result.has_images:
            img_dir = output_dir / "img"
            img_dir.mkdir(exist_ok=True)

            processed_images = await self.image_processor.process(
                result.images,
                source_name=name,
            )

            for image in processed_images:
                img_path = img_dir / image.filename
                async with aiofiles.open(img_path, "wb") as f:
                    await f.write(image.data)

            # Update result with processed images for metadata
            result.images = processed_images

            # Update markdown with renamed image filenames
            result.markdown = self._update_image_references(
                result.markdown, original_images, processed_images
            )

        # Write markdown
        md_path = output_dir / f"{name}.md"
        async with aiofiles.open(md_path, "w", encoding="utf-8") as f:
            await f.write(result.markdown)

        # Write metadata if enabled
        if self.config.generate_metadata:
            await self._write_metadata(result, output_dir / "metadata.json")

        return output_dir

    async def _write_metadata(self, result: ExtractionResult, path: Path) -> None:
        """Write metadata JSON file.

        Args:
            result: Extraction result
            path: Path to write metadata to
        """
        metadata = {
            "title": result.title,
            "source": result.source,
            "media_type": result.media_type.value if result.media_type else None,
            "charset": result.charset,
            "image_count": result.image_count,
            "images": [
                {
                    "filename": img.filename,
                    "format": img.format,
                    "page": img.page,
                    "caption": img.caption,
                    "description": img.description,
                    "size_bytes": img.size_bytes,
                }
                for img in result.images
            ],
            **result.metadata,
        }

        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(metadata, indent=2, ensure_ascii=False))

    def _clean_name(self, source: str) -> str:
        """Clean a source name for use as a directory/file name.

        Args:
            source: Source path or URL

        Returns:
            Cleaned name suitable for filesystem
        """
        # Handle URLs
        if source.startswith(("http://", "https://")):
            # Extract domain and path
            from urllib.parse import urlparse
            parsed = urlparse(source)
            name = parsed.netloc.replace(".", "_")
            if parsed.path and parsed.path != "/":
                path_part = parsed.path.strip("/").replace("/", "_")
                name = f"{name}_{path_part}"
        else:
            # File path - use stem + extension to avoid collisions
            # sample.wav -> sample_wav, sample.png -> sample_png
            p = Path(source)
            ext = p.suffix.lstrip(".").lower()
            name = f"{p.stem}_{ext}" if ext else p.stem

        # Clean characters
        name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)

        # Remove multiple underscores
        while "__" in name:
            name = name.replace("__", "_")

        # Limit length
        if len(name) > 100:
            name = name[:100]

        return name.strip("_")

    def _update_image_references(
        self,
        markdown: str,
        original_images: list,
        processed_images: list,
    ) -> str:
        """Update markdown image references with renamed filenames.

        Args:
            markdown: Original markdown content
            original_images: List of original ExtractedImage objects
            processed_images: List of processed ExtractedImage objects with new filenames

        Returns:
            Markdown with updated image references
        """
        if not original_images or not processed_images:
            return markdown

        # Build mapping from old filename to new filename
        filename_map = {}
        for orig, proc in zip(original_images, processed_images):
            if orig.filename != proc.filename:
                filename_map[orig.filename] = proc.filename

        if not filename_map:
            return markdown

        # Replace image references in markdown
        # Pattern matches ![alt](./img/filename) or ![alt](img/filename)
        def replace_image_ref(match: re.Match) -> str:
            alt_text = match.group(1)
            img_path = match.group(2)

            # Extract filename from path
            old_filename = Path(img_path).name

            if old_filename in filename_map:
                new_filename = filename_map[old_filename]
                # Preserve the path prefix (./img/ or img/)
                path_prefix = img_path.rsplit(old_filename, 1)[0]
                return f"![{alt_text}]({path_prefix}{new_filename})"

            return match.group(0)

        # Match markdown image syntax: ![alt](path)
        pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
        markdown = re.sub(pattern, replace_image_ref, markdown)

        return markdown


class OutputWriterSync:
    """Synchronous output writer for simpler use cases."""

    def __init__(self, config: IngestConfig | None = None):
        self.config = config or IngestConfig()
        self.image_processor = ImageProcessor(config)

    def write(self, result: ExtractionResult) -> Path:
        """Write an extraction result synchronously."""
        import asyncio
        writer = OutputWriter(self.config)
        return asyncio.run(writer.write(result))