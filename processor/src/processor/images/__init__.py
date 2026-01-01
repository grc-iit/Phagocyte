"""Image processing module for papers with VLM-generated descriptions.

This module handles:
- Reading figures.json metadata from paper directories
- Creating ImageChunk objects with captions and VLM descriptions
- Filtering out low-value figures (logos, etc.)
"""

from .processor import ImageProcessor

__all__ = ["ImageProcessor"]
