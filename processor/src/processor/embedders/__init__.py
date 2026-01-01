"""Embedding generators supporting multiple backends.

Backends:
- Ollama: Default backend for text/code (http://localhost:11434)
- Transformers: HuggingFace model support (sentence-transformers)
- OpenCLIP: Multimodal CLIP/SigLIP for image+text embeddings (transformers backend)
"""

from .base import BaseEmbedder
from .ollama import OllamaEmbedder
from .profiles import (
    EmbedderBackend,
    EmbeddingProfiles,
    ModelProfile,
    get_model_for_profile,
)


# Lazy imports for optional backends
def get_transformers_embedder():
    """Get TransformersEmbedder (requires sentence-transformers)."""
    from .transformers import TransformersEmbedder

    return TransformersEmbedder


def get_openclip_embedder():
    """Get OpenCLIPEmbedder (requires open-clip-torch)."""
    from .openclip import OpenCLIPEmbedder

    return OpenCLIPEmbedder


__all__ = [
    "BaseEmbedder",
    "OllamaEmbedder",
    "EmbedderBackend",
    "EmbeddingProfiles",
    "ModelProfile",
    "get_model_for_profile",
    "get_transformers_embedder",
    "get_openclip_embedder",
]
