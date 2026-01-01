"""RAG Processor: Chunking, embedding, and LanceDB loading."""

__version__ = "0.1.0"

from .types import Chunk, ContentType, ProcessingResult

__all__ = ["Chunk", "ContentType", "ProcessingResult", "__version__"]
