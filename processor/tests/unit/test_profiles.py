"""Unit tests for embedding profiles and backend selection."""

import pytest

from processor.embedders.profiles import (
    EmbedderBackend,
    EmbeddingProfiles,
    ModelProfile,
    get_model_for_profile,
)


class TestEmbedderBackend:
    """Test EmbedderBackend enum."""

    def test_backend_values(self) -> None:
        """Test backend enum values."""
        assert EmbedderBackend.OLLAMA.value == "ollama"
        assert EmbedderBackend.TRANSFORMERS.value == "transformers"

    def test_only_two_backends(self) -> None:
        """Test that only Ollama and Transformers backends exist."""
        backends = list(EmbedderBackend)
        assert len(backends) == 2
        assert EmbedderBackend.OLLAMA in backends
        assert EmbedderBackend.TRANSFORMERS in backends


class TestModelProfile:
    """Test ModelProfile dataclass."""

    def test_supports_ollama(self) -> None:
        """Test Ollama backend support detection."""
        profile = ModelProfile(
            name="test",
            ollama_model="test-model:latest",
            dimensions=768,
            context_length=512,
            description="Test",
        )

        assert profile.supports_backend(EmbedderBackend.OLLAMA) is True
        assert profile.supports_backend(EmbedderBackend.TRANSFORMERS) is False

    def test_supports_transformers_via_huggingface(self) -> None:
        """Test transformers support via HuggingFace ID."""
        profile = ModelProfile(
            name="test",
            huggingface_id="test/model",
            dimensions=768,
            context_length=512,
            description="Test",
        )

        assert profile.supports_backend(EmbedderBackend.TRANSFORMERS) is True
        assert profile.supports_backend(EmbedderBackend.OLLAMA) is False

    def test_supports_transformers_via_openclip(self) -> None:
        """Test transformers support via OpenCLIP model."""
        profile = ModelProfile(
            name="test",
            dimensions=1024,
            context_length=77,
            description="Test",
            is_multimodal=True,
            open_clip_model="ViT-H-14",
            open_clip_pretrained="laion2b",
        )

        assert profile.supports_backend(EmbedderBackend.TRANSFORMERS) is True
        assert profile.supports_backend(EmbedderBackend.OLLAMA) is False

    def test_supports_both_backends(self) -> None:
        """Test model supporting both backends."""
        profile = ModelProfile(
            name="test",
            ollama_model="test-model:latest",
            huggingface_id="test/model",
            dimensions=768,
            context_length=512,
            description="Test",
        )

        assert profile.supports_backend(EmbedderBackend.OLLAMA) is True
        assert profile.supports_backend(EmbedderBackend.TRANSFORMERS) is True

    def test_multimodal_flag(self) -> None:
        """Test multimodal flag on profile."""
        text_profile = ModelProfile(
            name="text",
            dimensions=768,
            context_length=512,
            description="Text model",
        )
        assert text_profile.is_multimodal is False

        multimodal_profile = ModelProfile(
            name="clip",
            dimensions=768,
            context_length=77,
            description="CLIP model",
            is_multimodal=True,
            open_clip_model="ViT-L-14",
        )
        assert multimodal_profile.is_multimodal is True


class TestEmbeddingProfiles:
    """Test EmbeddingProfiles class."""

    def test_text_profiles_exist(self) -> None:
        """Test that text profiles are defined."""
        profiles = EmbeddingProfiles.TEXT_PROFILES

        assert "high" in profiles
        assert "medium" in profiles
        assert "low" in profiles

    def test_code_profiles_exist(self) -> None:
        """Test that code profiles are defined."""
        profiles = EmbeddingProfiles.CODE_PROFILES

        assert "high" in profiles
        assert "low" in profiles

    def test_multimodal_profiles_exist(self) -> None:
        """Test that multimodal profiles are defined."""
        profiles = EmbeddingProfiles.MULTIMODAL_PROFILES

        assert "high" in profiles
        assert "low" in profiles

    def test_text_profiles_have_ollama_models(self) -> None:
        """Test that text profiles have Ollama model names."""
        for name, profile in EmbeddingProfiles.TEXT_PROFILES.items():
            assert profile.ollama_model, f"Text profile {name} missing ollama_model"

    def test_code_profiles_have_ollama_models(self) -> None:
        """Test that code profiles have Ollama model names."""
        for name, profile in EmbeddingProfiles.CODE_PROFILES.items():
            assert profile.ollama_model, f"Code profile {name} missing ollama_model"

    def test_multimodal_profiles_use_transformers(self) -> None:
        """Test that multimodal profiles use transformers (no Ollama)."""
        for name, profile in EmbeddingProfiles.MULTIMODAL_PROFILES.items():
            assert profile.is_multimodal, f"Multimodal profile {name} missing is_multimodal"
            assert profile.open_clip_model, f"Multimodal profile {name} missing open_clip_model"
            assert not profile.ollama_model, f"Multimodal profile {name} should not have ollama_model"

    def test_get_text_profile(self) -> None:
        """Test getting text embedding profile."""
        low = EmbeddingProfiles.get_text_profile("low")
        assert low.name == "Qwen3-Embedding-0.6B"
        assert low.ollama_model == "qwen3-embedding:0.6b"
        assert low.dimensions == 1024

        high = EmbeddingProfiles.get_text_profile("high")
        assert high.name == "Qwen3-Embedding-8B"
        assert high.ollama_model == "qwen3-embedding:8b"
        assert high.dimensions == 4096

    def test_get_code_profile(self) -> None:
        """Test getting code embedding profile."""
        low = EmbeddingProfiles.get_code_profile("low")
        assert low.name == "jina-code-embeddings-0.5b"
        assert low.dimensions == 896

        high = EmbeddingProfiles.get_code_profile("high")
        assert high.name == "jina-code-embeddings-1.5b"
        assert high.dimensions == 1536

    def test_get_multimodal_profile(self) -> None:
        """Test getting multimodal embedding profile."""
        low = EmbeddingProfiles.get_multimodal_profile("low")
        assert low.is_multimodal is True
        assert "CLIP" in low.name
        assert low.dimensions == 768

        high = EmbeddingProfiles.get_multimodal_profile("high")
        assert high.is_multimodal is True
        assert "CLIP" in high.name
        assert high.dimensions == 1024

    def test_list_profiles(self) -> None:
        """Test listing available profiles."""
        text = EmbeddingProfiles.list_text_profiles()
        assert "low" in text
        assert "medium" in text
        assert "high" in text

        code = EmbeddingProfiles.list_code_profiles()
        assert "low" in code
        assert "high" in code

        multimodal = EmbeddingProfiles.list_multimodal_profiles()
        assert "low" in multimodal
        assert "high" in multimodal

    def test_fallback_profile(self) -> None:
        """Test fallback profile configuration."""
        fallback = EmbeddingProfiles.FALLBACK

        assert fallback.name == "Qwen3-Embedding-0.6B"
        assert fallback.ollama_model == "qwen3-embedding:0.6b"
        assert fallback.huggingface_id == "Qwen/Qwen3-Embedding-0.6B"

    def test_invalid_profile_returns_default(self) -> None:
        """Test that invalid profile names return the default (low)."""
        text = EmbeddingProfiles.get_text_profile("nonexistent")
        assert text.name == "Qwen3-Embedding-0.6B"

        code = EmbeddingProfiles.get_code_profile("nonexistent")
        assert code.name == "jina-code-embeddings-0.5b"

        multimodal = EmbeddingProfiles.get_multimodal_profile("nonexistent")
        assert multimodal.name == "CLIP-ViT-L-14"


class TestGetModelForProfile:
    """Test get_model_for_profile function."""

    def test_text_auto_selects_ollama(self) -> None:
        """Test that text domain auto-selects Ollama backend."""
        profile, backend = get_model_for_profile("text", "low")

        assert profile.name == "Qwen3-Embedding-0.6B"
        assert backend == EmbedderBackend.OLLAMA

    def test_code_auto_selects_ollama(self) -> None:
        """Test that code domain auto-selects Ollama backend."""
        profile, backend = get_model_for_profile("code", "low")

        assert profile.name == "jina-code-embeddings-0.5b"
        assert backend == EmbedderBackend.OLLAMA

    def test_multimodal_auto_selects_transformers(self) -> None:
        """Test that multimodal domain auto-selects Transformers backend."""
        profile, backend = get_model_for_profile("multimodal", "low")

        assert profile.name == "CLIP-ViT-L-14"
        assert profile.is_multimodal is True
        assert backend == EmbedderBackend.TRANSFORMERS

    def test_explicit_transformers_for_text(self) -> None:
        """Test explicit transformers backend for text."""
        profile, backend = get_model_for_profile(
            "text", "low", EmbedderBackend.TRANSFORMERS
        )

        # Should work because Qwen has huggingface_id
        assert backend == EmbedderBackend.TRANSFORMERS
        assert profile.huggingface_id == "Qwen/Qwen3-Embedding-0.6B"

    def test_explicit_transformers_for_code(self) -> None:
        """Test explicit transformers backend for code."""
        profile, backend = get_model_for_profile(
            "code", "low", EmbedderBackend.TRANSFORMERS
        )

        # Should work because jina has huggingface_id
        assert backend == EmbedderBackend.TRANSFORMERS
        assert profile.huggingface_id == "jinaai/jina-code-embeddings-0.5b"

    def test_invalid_domain_uses_fallback(self) -> None:
        """Test that invalid domain uses fallback profile."""
        profile, backend = get_model_for_profile("invalid", "any")

        assert profile.name == "Qwen3-Embedding-0.6B"
        assert backend == EmbedderBackend.OLLAMA

    def test_invalid_profile_uses_default(self) -> None:
        """Test that invalid profile uses default for domain."""
        profile, _ = get_model_for_profile("text", "nonexistent")
        assert profile.name == "Qwen3-Embedding-0.6B"

        profile, _ = get_model_for_profile("code", "nonexistent")
        assert profile.name == "jina-code-embeddings-0.5b"

    def test_none_backend_uses_auto_selection(self) -> None:
        """Test that None backend triggers auto-selection."""
        # Text -> Ollama
        _, backend = get_model_for_profile("text", "low", None)
        assert backend == EmbedderBackend.OLLAMA

        # Code -> Ollama
        _, backend = get_model_for_profile("code", "low", None)
        assert backend == EmbedderBackend.OLLAMA

        # Multimodal -> Transformers
        _, backend = get_model_for_profile("multimodal", "low", None)
        assert backend == EmbedderBackend.TRANSFORMERS

    def test_backend_fallback_when_unsupported(self) -> None:
        """Test fallback to other backend when requested one unsupported."""
        # Multimodal doesn't support Ollama, should fallback to Transformers
        profile, backend = get_model_for_profile(
            "multimodal", "low", EmbedderBackend.OLLAMA
        )
        assert backend == EmbedderBackend.TRANSFORMERS
        assert profile.is_multimodal is True
