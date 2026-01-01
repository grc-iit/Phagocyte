"""Transformers/sentence-transformers embedding client.

Supports all HuggingFace embedding models including:
- Text: Qwen3-Embedding, stella, etc.
- Code: jina-code-embeddings (0.5b, 1.5b)

Requires: sentence-transformers, torch
"""

import asyncio

from .base import BaseEmbedder


class TransformersEmbedder(BaseEmbedder):
    """Embedding generator using sentence-transformers.

    Supports any HuggingFace embedding model. Recommended for:
    - jina-code-embeddings (not available on Ollama)
    - High-quality text models when Ollama is unavailable
    """

    def __init__(
        self,
        model: str = "jinaai/jina-code-embeddings-0.5b",
        device: str = "auto",
        torch_dtype: str = "bfloat16",
        use_flash_attention: bool = True,
        trust_remote_code: bool = True,
    ):
        """Initialize transformers embedder.

        Args:
            model: HuggingFace model ID
            device: Device to use ('auto', 'cuda', 'cpu', 'cuda:0', etc.)
            torch_dtype: Torch dtype ('float32', 'float16', 'bfloat16')
            use_flash_attention: Use flash attention 2 if available
            trust_remote_code: Trust remote code for model loading
        """
        self.model_id = model
        self.device = device
        self.torch_dtype_str = torch_dtype
        self.use_flash_attention = use_flash_attention
        self.trust_remote_code = trust_remote_code

        self._model: SentenceTransformer | None = None
        self._dimensions: int | None = None

    def _get_model(self) -> "SentenceTransformer":
        """Lazy load the model."""
        if self._model is None:
            try:
                import torch
                from sentence_transformers import SentenceTransformer
            except ImportError as e:
                raise ImportError(
                    "sentence-transformers and torch required. "
                    "Install with: pip install sentence-transformers torch"
                ) from e

            # Determine torch dtype
            dtype_map = {
                "float32": torch.float32,
                "float16": torch.float16,
                "bfloat16": torch.bfloat16,
            }
            torch_dtype = dtype_map.get(self.torch_dtype_str, torch.bfloat16)

            # Build model kwargs
            model_kwargs = {
                "torch_dtype": torch_dtype,
                "trust_remote_code": self.trust_remote_code,
            }

            # Add flash attention if requested and available
            if self.use_flash_attention:
                try:
                    import flash_attn  # noqa: F401

                    model_kwargs["attn_implementation"] = "flash_attention_2"
                except ImportError:
                    pass  # Flash attention not available, continue without it

            # Handle device
            if self.device == "auto":
                if torch.cuda.is_available():
                    model_kwargs["device_map"] = "cuda"
                else:
                    model_kwargs["device_map"] = "cpu"
            else:
                model_kwargs["device_map"] = self.device

            # Load model
            self._model = SentenceTransformer(
                self.model_id,
                model_kwargs=model_kwargs,
                tokenizer_kwargs={"padding_side": "left"},
            )

            # Get dimensions from model
            self._dimensions = self._model.get_sentence_embedding_dimension()

        return self._model

    @property
    def dimensions(self) -> int:
        """Get embedding dimensions."""
        if self._dimensions is None:
            self._get_model()
        return self._dimensions or 768

    async def embed(self, text: str) -> list[float]:
        """Generate embedding for single text."""
        model = self._get_model()

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(
            None,
            lambda: model.encode(text, convert_to_numpy=True).tolist(),
        )
        return embedding

    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 32,
        prompt_name: str | None = None,
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
            prompt_name: Optional prompt name for task-specific embeddings
                        (e.g., 'nl2code_query', 'nl2code_document' for jina-code)
        """
        model = self._get_model()

        def _encode():
            kwargs = {
                "batch_size": batch_size,
                "convert_to_numpy": True,
                "show_progress_bar": False,
            }
            if prompt_name:
                kwargs["prompt_name"] = prompt_name

            embeddings = model.encode(texts, **kwargs)
            return [emb.tolist() for emb in embeddings]

        # Run in thread pool
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(None, _encode)
        return embeddings

    async def is_available(self) -> bool:
        """Check if transformers backend is available."""
        try:
            import sentence_transformers  # noqa: F401
            import torch  # noqa: F401

            return True
        except ImportError:
            return False

    async def model_exists(self, model_name: str | None = None) -> bool:
        """Check if model can be loaded (may download if not cached)."""
        model_id = model_name or self.model_id

        try:
            from huggingface_hub import model_info

            info = model_info(model_id)
            return info is not None
        except Exception:
            return False

    async def close(self) -> None:
        """Release model resources."""
        if self._model is not None:
            # Clear CUDA cache if using GPU
            try:
                import torch

                if torch.cuda.is_available():
                    del self._model
                    self._model = None
                    torch.cuda.empty_cache()
            except Exception:
                pass
            self._model = None
