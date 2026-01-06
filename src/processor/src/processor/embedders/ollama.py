"""Ollama embedding client using the REST API."""

import asyncio

import httpx

from .base import BaseEmbedder


class OllamaEmbedder(BaseEmbedder):
    """Embedding generator using Ollama's REST API.

    Uses Ollama's /api/embeddings endpoint for generating embeddings.
    Requires Ollama to be running with the specified model pulled.
    """

    def __init__(
        self,
        model: str = "qwen3-embedding:0.6b",
        host: str = "http://localhost:11434",
        timeout: float = 120.0,
    ):
        """Initialize Ollama embedder.

        Args:
            model: Ollama model name (e.g., "qwen3-embedding:0.6b")
            host: Ollama server URL
            timeout: Request timeout in seconds
        """
        self.model_name = model
        self.host = host.rstrip("/")
        self.timeout = timeout
        self.dimensions = 0  # Will be set from first response
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def embed(self, text: str, max_retries: int = 3) -> list[float]:
        """Generate embedding for single text.

        Args:
            text: Text to embed
            max_retries: Number of retry attempts on failure

        Returns:
            Embedding vector as list of floats
        """
        client = self._get_client()

        # Truncate very long texts to avoid issues
        max_chars = 8000  # ~2000 tokens
        if len(text) > max_chars:
            text = text[:max_chars]

        for attempt in range(max_retries):
            try:
                response = await client.post(
                    f"{self.host}/api/embeddings",
                    json={"model": self.model_name, "prompt": text},
                )
                response.raise_for_status()
                data = response.json()
                embedding = data["embedding"]

                # Update dimensions from actual response
                if self.dimensions == 0:
                    self.dimensions = len(embedding)

                return embedding
            except Exception:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1.0 * (attempt + 1))
                else:
                    raise

        # Should never reach here due to raise, but satisfy mypy
        return []

    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 32,
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Ollama's API doesn't support batch embedding, so we process
        texts sequentially to avoid overwhelming the server.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts per batch (processed sequentially within)

        Returns:
            List of embedding vectors
        """
        embeddings: list[list[float]] = []

        for i, text in enumerate(texts):
            embedding = await self.embed(text)
            embeddings.append(embedding)
            # Add small delay to prevent server overload
            if (i + 1) % 10 == 0:
                await asyncio.sleep(0.1)

        return embeddings

    async def is_available(self) -> bool:
        """Check if Ollama server is available."""
        try:
            client = self._get_client()
            response = await client.get(f"{self.host}/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        """List available models in Ollama."""
        try:
            client = self._get_client()
            response = await client.get(f"{self.host}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception:
            return []

    async def model_exists(self, model_name: str) -> bool:
        """Check if a model is available in Ollama.

        Args:
            model_name: Model name to check

        Returns:
            True if model is available
        """
        models = await self.list_models()
        # Check both exact match and partial match
        return any(model_name in m or m in model_name for m in models)

    @staticmethod
    def pull_model(model_name: str) -> tuple[bool, str]:
        """Pull a model using ollama CLI.

        Args:
            model_name: Model name to pull (e.g., "qwen3-embedding:0.6b")

        Returns:
            Tuple of (success, output_message)
        """
        import subprocess

        try:
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=1800,  # 30 minute timeout for large models
            )
            output = result.stdout + result.stderr
            return result.returncode == 0, output.strip()
        except subprocess.TimeoutExpired:
            return False, "Download timed out"
        except FileNotFoundError:
            return False, "ollama CLI not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def is_cli_available() -> bool:
        """Check if ollama CLI is available."""
        import subprocess

        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False

    async def close(self) -> None:
        """Close HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
