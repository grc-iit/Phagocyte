"""OpenCLIP embedding client for multimodal (image + text) embeddings.

Supports CLIP and SigLIP models for unified table approach where
text, code, and images can all be embedded into the same vector space.

Requires: open-clip-torch, torch, PIL
"""

import asyncio
from pathlib import Path

from .base import BaseEmbedder


class OpenCLIPEmbedder(BaseEmbedder):
    """Embedding generator using OpenCLIP for multimodal content.

    Supports:
    - DFN-CLIP ViT-H-14-378 (ImageNet 84.4%)
    - SigLIP ViT-SO400M-14 (ImageNet 82%)

    Can embed both text AND images into the same vector space,
    enabling cross-modal search (find images from text queries).
    """

    def __init__(
        self,
        model_name: str = "ViT-SO400M-14-SigLIP",
        pretrained: str = "webli",
        device: str = "auto",
    ):
        """Initialize OpenCLIP embedder.

        Args:
            model_name: OpenCLIP model name (e.g., 'ViT-H-14-378-quickgelu', 'ViT-SO400M-14-SigLIP')
            pretrained: Pretrained weights name (e.g., 'dfn5b', 'webli')
            device: Device to use ('auto', 'cuda', 'cpu')
        """
        self.model_name = model_name
        self.pretrained = pretrained
        self.device_str = device

        self._model = None
        self._preprocess = None
        self._tokenizer = None
        self._device = None
        self._dimensions: int | None = None

    def _get_model(self):
        """Lazy load the model."""
        if self._model is None:
            try:
                import open_clip
                import torch
            except ImportError as e:
                raise ImportError(
                    "open-clip-torch and torch required. "
                    "Install with: pip install open-clip-torch torch"
                ) from e

            # Determine device
            if self.device_str == "auto":
                self._device = "cuda" if torch.cuda.is_available() else "cpu"
            else:
                self._device = self.device_str

            # Load model
            self._model, self._preprocess = open_clip.create_model_from_pretrained(
                f"hf-hub:{self._get_hf_hub_id()}"
                if self._is_hf_model()
                else self.model_name,
                pretrained=self.pretrained if not self._is_hf_model() else None,
                device=self._device,
            )

            # Get tokenizer
            self._tokenizer = open_clip.get_tokenizer(self.model_name)

            # Set to eval mode
            self._model.eval()

            # Get dimensions
            with torch.no_grad():
                dummy_text = self._tokenizer(["test"])
                if self._device:
                    dummy_text = dummy_text.to(self._device)
                text_features = self._model.encode_text(dummy_text)
                self._dimensions = text_features.shape[-1]

        return self._model

    def _is_hf_model(self) -> bool:
        """Check if this is a HuggingFace Hub model."""
        # Models with specific pretrained weights from HF
        hf_models = {
            ("ViT-H-14-378-quickgelu", "dfn5b"): "apple/DFN5B-CLIP-ViT-H-14-378",
        }
        return (self.model_name, self.pretrained) in hf_models

    def _get_hf_hub_id(self) -> str:
        """Get HuggingFace Hub ID for this model."""
        hf_models = {
            ("ViT-H-14-378-quickgelu", "dfn5b"): "apple/DFN5B-CLIP-ViT-H-14-378",
        }
        return hf_models.get((self.model_name, self.pretrained), "")

    @property
    def dimensions(self) -> int:
        """Get embedding dimensions."""
        if self._dimensions is None:
            self._get_model()
        return self._dimensions or 1024

    async def embed(self, text: str) -> list[float]:
        """Generate embedding for text."""
        embeddings = await self.embed_texts([text])
        return embeddings[0]

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        import torch
        import torch.nn.functional as F

        model = self._get_model()

        def _encode():
            tokens = self._tokenizer(texts)
            if self._device:
                tokens = tokens.to(self._device)

            with torch.no_grad():
                text_features = model.encode_text(tokens)
                text_features = F.normalize(text_features, dim=-1)

            # Convert to float32 for numpy compatibility
            return text_features.float().cpu().numpy().tolist()

        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(None, _encode)
        return embeddings

    async def embed_image(self, image_path: str | Path) -> list[float]:
        """Generate embedding for an image.

        Args:
            image_path: Path to image file

        Returns:
            Image embedding vector
        """
        embeddings = await self.embed_images([image_path])
        return embeddings[0]

    async def embed_images(
        self, image_paths: list[str | Path]
    ) -> list[list[float]]:
        """Generate embeddings for multiple images.

        Args:
            image_paths: List of paths to image files

        Returns:
            List of image embedding vectors
        """
        import torch
        import torch.nn.functional as F
        from PIL import Image

        model = self._get_model()

        def _encode():
            images = []
            for path in image_paths:
                img = Image.open(path).convert("RGB")
                img_tensor = self._preprocess(img)
                images.append(img_tensor)

            image_input = torch.stack(images)
            if self._device:
                image_input = image_input.to(self._device)

            with torch.no_grad():
                image_features = model.encode_image(image_input)
                image_features = F.normalize(image_features, dim=-1)

            # Convert to float32 for numpy compatibility
            return image_features.float().cpu().numpy().tolist()

        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(None, _encode)
        return embeddings

    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 32,
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts with batching."""
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_embeddings = await self.embed_texts(batch)
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    async def is_available(self) -> bool:
        """Check if OpenCLIP backend is available."""
        try:
            import open_clip  # noqa: F401
            import torch  # noqa: F401

            return True
        except ImportError:
            return False

    async def model_exists(self, model_name: str | None = None) -> bool:
        """Check if model is available in open_clip."""
        try:
            import open_clip

            pretrained_models = open_clip.list_pretrained()
            model = model_name or self.model_name

            # Check if model/pretrained combo exists
            return any(
                model.lower() in m[0].lower() or model.lower() in m[1].lower()
                for m in pretrained_models
            )
        except Exception:
            return False

    async def close(self) -> None:
        """Release model resources."""
        if self._model is not None:
            try:
                import torch

                if torch.cuda.is_available():
                    del self._model
                    self._model = None
                    self._preprocess = None
                    self._tokenizer = None
                    torch.cuda.empty_cache()
            except Exception:
                pass
            self._model = None
