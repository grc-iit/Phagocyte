"""Embedding model profile definitions.

Backend support:
- Ollama: Default backend for text and code embeddings (GGUF models)
- Transformers: For multimodal (CLIP/SigLIP), or when user explicitly chooses

Text/Code embeddings use Ollama by default for simplicity and performance.
Multimodal embeddings require the transformers backend (OpenCLIP).

Users can override the backend via config to use transformers for text/code
if they prefer HuggingFace models directly.
"""

from dataclasses import dataclass
from enum import Enum


class EmbedderBackend(Enum):
    """Available embedding backends."""

    OLLAMA = "ollama"  # Default: Ollama for text/code embeddings
    TRANSFORMERS = "transformers"  # For multimodal, or user override


@dataclass
class ModelProfile:
    """Configuration for an embedding model.

    Each profile can support one or both backends:
    - ollama_model: Model name for Ollama API (e.g., "qwen3-embedding:0.6b")
    - huggingface_id: Model ID for transformers/sentence-transformers

    For multimodal models, use open_clip_model and open_clip_pretrained instead.
    """

    name: str
    dimensions: int
    context_length: int
    description: str

    # Ollama configuration (primary for text/code)
    ollama_model: str = ""

    # Transformers/HuggingFace configuration (alternative, or for multimodal)
    huggingface_id: str = ""

    # OpenCLIP for multimodal embeddings (text + image in same space)
    is_multimodal: bool = False
    open_clip_model: str = ""
    open_clip_pretrained: str = ""

    def supports_backend(self, backend: EmbedderBackend) -> bool:
        """Check if this model supports a given backend."""
        if backend == EmbedderBackend.OLLAMA:
            return bool(self.ollama_model)
        elif backend == EmbedderBackend.TRANSFORMERS:
            return bool(self.huggingface_id) or bool(self.open_clip_model)
        return False


class EmbeddingProfiles:
    """Embedding model profiles organized by domain and resource level.

    Profiles:
    - TEXT_PROFILES: For documents, papers, markdown (Qwen3-Embedding)
    - CODE_PROFILES: For source code (jina-code-embeddings)
    - MULTIMODAL_PROFILES: For images + text in unified space (CLIP/SigLIP)
    """

    # =========================================================================
    # TEXT EMBEDDING PROFILES
    # Qwen3-Embedding: #1 MTEB multilingual, 100+ languages, 32K context
    # Default: Ollama, can switch to transformers via config
    # =========================================================================
    TEXT_PROFILES = {
        "high": ModelProfile(
            name="Qwen3-Embedding-8B",
            ollama_model="qwen3-embedding:8b",
            huggingface_id="Qwen/Qwen3-Embedding-8B",
            dimensions=4096,
            context_length=32768,
            description="MTEB 70.58, #1 multilingual, 100+ languages",
        ),
        "medium": ModelProfile(
            name="Qwen3-Embedding-4B",
            ollama_model="qwen3-embedding:4b",
            huggingface_id="Qwen/Qwen3-Embedding-4B",
            dimensions=2560,
            context_length=32768,
            description="Balanced 4B model, 32K context",
        ),
        "low": ModelProfile(
            name="Qwen3-Embedding-0.6B",
            ollama_model="qwen3-embedding:0.6b",
            huggingface_id="Qwen/Qwen3-Embedding-0.6B",
            dimensions=1024,
            context_length=32768,
            description="Compact 0.6B, fast inference, 32K context",
        ),
    }

    # =========================================================================
    # CODE EMBEDDING PROFILES
    # jina-code-embeddings (2025): SOTA code retrieval, 15+ languages
    # Based on Qwen2.5-Coder, supports NL2Code, Code2Code, Code2NL
    # Default: Ollama, can switch to transformers via config
    # =========================================================================
    CODE_PROFILES = {
        "high": ModelProfile(
            name="jina-code-embeddings-1.5b",
            ollama_model="hf.co/jinaai/jina-code-embeddings-1.5b-GGUF:Q8_0",
            huggingface_id="jinaai/jina-code-embeddings-1.5b",
            dimensions=1536,
            context_length=32768,
            description="SOTA 79.04% code retrieval, 15+ languages",
        ),
        "low": ModelProfile(
            name="jina-code-embeddings-0.5b",
            ollama_model="hf.co/jinaai/jina-code-embeddings-0.5b-GGUF:Q8_0",
            huggingface_id="jinaai/jina-code-embeddings-0.5b",
            dimensions=896,
            context_length=32768,
            description="SOTA 78.41% code retrieval, compact 0.5B",
        ),
    }

    # =========================================================================
    # MULTIMODAL EMBEDDING PROFILES
    # CLIP/SigLIP: Embed text and images into the same vector space
    # Always uses transformers backend (OpenCLIP) - no Ollama support
    # =========================================================================
    MULTIMODAL_PROFILES = {
        "high": ModelProfile(
            name="CLIP-ViT-H-14",
            huggingface_id="laion/CLIP-ViT-H-14-laion2B-s32B-b79K",
            dimensions=1024,
            context_length=77,  # CLIP text token limit
            description="CLIP ViT-H-14, highest quality",
            is_multimodal=True,
            open_clip_model="ViT-H-14",
            open_clip_pretrained="laion2b_s32b_b79k",
        ),
        "low": ModelProfile(
            name="CLIP-ViT-L-14",
            huggingface_id="laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
            dimensions=768,
            context_length=77,
            description="CLIP ViT-L-14, good balance of quality/speed",
            is_multimodal=True,
            open_clip_model="ViT-L-14",
            open_clip_pretrained="laion2b_s32b_b82k",
        ),
    }

    # =========================================================================
    # FALLBACK PROFILE
    # Used when domain is unknown or profile not found
    # =========================================================================
    FALLBACK = ModelProfile(
        name="Qwen3-Embedding-0.6B",
        ollama_model="qwen3-embedding:0.6b",
        huggingface_id="Qwen/Qwen3-Embedding-0.6B",
        dimensions=1024,
        context_length=32768,
        description="Lightweight fallback, 32K context",
    )

    @classmethod
    def get_text_profile(cls, profile: str) -> ModelProfile:
        """Get text embedding profile by name."""
        return cls.TEXT_PROFILES.get(profile, cls.TEXT_PROFILES["low"])

    @classmethod
    def get_code_profile(cls, profile: str) -> ModelProfile:
        """Get code embedding profile by name."""
        return cls.CODE_PROFILES.get(profile, cls.CODE_PROFILES["low"])

    @classmethod
    def get_multimodal_profile(cls, profile: str) -> ModelProfile:
        """Get multimodal embedding profile by name."""
        return cls.MULTIMODAL_PROFILES.get(profile, cls.MULTIMODAL_PROFILES["low"])

    @classmethod
    def list_text_profiles(cls) -> list[str]:
        """List available text profile names."""
        return list(cls.TEXT_PROFILES.keys())

    @classmethod
    def list_code_profiles(cls) -> list[str]:
        """List available code profile names."""
        return list(cls.CODE_PROFILES.keys())

    @classmethod
    def list_multimodal_profiles(cls) -> list[str]:
        """List available multimodal profile names."""
        return list(cls.MULTIMODAL_PROFILES.keys())


def get_model_for_profile(
    domain: str,
    profile: str,
    backend: EmbedderBackend | None = None,
) -> tuple[ModelProfile, EmbedderBackend]:
    """Get model profile and backend for a domain/profile combination.

    Args:
        domain: 'text', 'code', or 'multimodal'
        profile: Profile name ('low', 'medium', 'high')
        backend: Explicit backend choice, or None for automatic selection

    Returns:
        Tuple of (ModelProfile, EmbedderBackend)

    Automatic backend selection:
    - text/code: OLLAMA (can be overridden to TRANSFORMERS)
    - multimodal: TRANSFORMERS (CLIP requires OpenCLIP, no Ollama support)
    """
    # Get the profile for the domain
    if domain == "text":
        model_profile = EmbeddingProfiles.get_text_profile(profile)
    elif domain == "code":
        model_profile = EmbeddingProfiles.get_code_profile(profile)
    elif domain == "multimodal":
        model_profile = EmbeddingProfiles.get_multimodal_profile(profile)
    else:
        model_profile = EmbeddingProfiles.FALLBACK

    # Determine backend
    if backend is None:
        # Auto-select: multimodal needs transformers, others use Ollama
        if model_profile.is_multimodal:
            backend = EmbedderBackend.TRANSFORMERS
        else:
            backend = EmbedderBackend.OLLAMA

    # Verify the model supports the requested backend
    if not model_profile.supports_backend(backend):
        # Try to fall back to the other backend
        other = (
            EmbedderBackend.TRANSFORMERS
            if backend == EmbedderBackend.OLLAMA
            else EmbedderBackend.OLLAMA
        )
        if model_profile.supports_backend(other):
            backend = other
        else:
            # Neither backend works, use fallback profile
            model_profile = EmbeddingProfiles.FALLBACK
            backend = EmbedderBackend.OLLAMA

    return model_profile, backend
