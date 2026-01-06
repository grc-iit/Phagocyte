"""Base embedder class for generating embeddings."""

from abc import ABC, abstractmethod

from ..types import Chunk


class BaseEmbedder(ABC):
    """Abstract base class for embedding generators."""

    model_name: str
    dimensions: int

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        pass

    @abstractmethod
    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 32,
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts per batch

        Returns:
            List of embedding vectors
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the embedding service is available."""
        pass

    async def embed_chunks(
        self,
        chunks: list[Chunk],
        batch_size: int = 32,
    ) -> list[Chunk]:
        """Embed a list of chunks, modifying them in place.

        Args:
            chunks: Chunks to embed
            batch_size: Batch size for embedding

        Returns:
            Chunks with embeddings attached
        """
        texts = [c.content for c in chunks]
        embeddings = await self.embed_batch(texts, batch_size)

        for chunk, embedding in zip(chunks, embeddings, strict=False):
            chunk.embedding = embedding

        return chunks

    @abstractmethod
    async def close(self) -> None:
        """Close any open connections."""
        ...
