"""RAG MCP server configuration.

Provides configuration schema for the RAG MCP server, including
settings for retrieval-time optimizations like HyDE and reranking.
"""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class HyDEConfig(BaseModel):
    """HyDE (Hypothetical Document Embeddings) configuration.

    HyDE transforms the query by generating a hypothetical answer
    and embedding that instead of the raw query. Works well for
    knowledge-seeking questions.

    Supports two backends:
    - claude_sdk: Uses Claude Code Agent SDK (default, best when used with Claude)
    - ollama: Uses local Ollama models (fallback for standalone use)
    """

    enabled: bool = Field(default=False, description="Enable HyDE by default")
    backend: str = Field(
        default="claude_sdk",
        description="Backend for generation: claude_sdk (default) or ollama",
    )
    # Claude SDK settings
    claude_model: str = Field(
        default="haiku",
        description="Claude model for generation: haiku (fast), sonnet, opus",
    )
    # Ollama settings (fallback)
    ollama_model: str = Field(
        default="llama3.2:latest",
        description="Ollama model for hypothetical generation (fallback)",
    )
    prompt_template: str = Field(
        default="Write a short passage that directly answers this question: {query}",
        description="Prompt template for generation",
    )
    max_tokens: int = Field(default=256, description="Maximum tokens to generate")


class RerankerConfig(BaseModel):
    """Cross-encoder reranking configuration.

    Reranking retrieves more candidates than needed, then uses a
    cross-encoder model to score query-document pairs more accurately.
    Significantly improves precision at the cost of latency.
    """

    enabled: bool = Field(default=False, description="Enable reranking by default")
    model: str = Field(
        default="BAAI/bge-reranker-v2-m3",
        description="Cross-encoder model from HuggingFace",
    )
    top_k: int = Field(default=20, description="Retrieve this many candidates")
    top_n: int = Field(default=5, description="Return this many after reranking")
    device: str = Field(default="auto", description="Device for inference (auto/cuda/cpu)")


class QueryExpansionConfig(BaseModel):
    """Query expansion configuration.

    Expands the query with related terms to improve recall.

    Supports two backends:
    - claude_sdk: Uses Claude Code Agent SDK (default)
    - ollama: Uses local Ollama models (fallback)
    """

    enabled: bool = Field(default=False, description="Enable query expansion by default")
    backend: str = Field(
        default="claude_sdk",
        description="Backend for expansion: claude_sdk (default) or ollama",
    )
    claude_model: str = Field(
        default="haiku",
        description="Claude model for expansion: haiku (fast), sonnet, opus",
    )
    ollama_model: str = Field(
        default="llama3.2:latest",
        description="Ollama model for expansion (fallback)",
    )
    prompt_template: str = Field(
        default="Generate 3 related search terms for: {query}",
        description="Prompt template for expansion",
    )


class RAGConfig(BaseModel):
    """Main RAG MCP configuration.

    Controls all aspects of the RAG search server including
    embedding profiles, default search behavior, and optimizations.
    """

    # Database
    default_db_path: str = Field(
        default="./lancedb", description="Default database path"
    )

    # Embedding (must match processor config for consistency)
    text_profile: str = Field(
        default="low", description="Text embedding profile (low/medium/high)"
    )
    code_profile: str = Field(
        default="low", description="Code embedding profile (low/high)"
    )
    ollama_host: str = Field(
        default="http://localhost:11434", description="Ollama server URL"
    )

    # Search defaults
    default_limit: int = Field(default=5, description="Default number of results")
    default_hybrid: bool = Field(
        default=False, description="Use hybrid search by default"
    )

    # Optimizations
    hyde: HyDEConfig = Field(default_factory=HyDEConfig)
    reranker: RerankerConfig = Field(default_factory=RerankerConfig)
    query_expansion: QueryExpansionConfig = Field(default_factory=QueryExpansionConfig)

    # Parent expansion
    expand_parents: bool = Field(
        default=False, description="Expand to parent documents by default"
    )

    @classmethod
    def from_yaml(cls, path: Path) -> "RAGConfig":
        """Load configuration from YAML file.

        Args:
            path: Path to YAML config file

        Returns:
            RAGConfig instance
        """
        if not path.exists():
            return cls()
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)

    def to_yaml(self, path: Path) -> None:
        """Save configuration to YAML file with comments.

        Args:
            path: Output path for YAML config
        """
        content = f"""# RAG MCP Configuration
# Generated by: uv run rag-mcp --config_generate
#
# This config controls the RAG search server behavior.
# Embedding profiles MUST match the processor config used to build the database.

# Database Settings
default_db_path: "{self.default_db_path}"

# Embedding Profiles (must match processor config)
text_profile: "{self.text_profile}"  # low (0.6B), medium (4B), high (8B)
code_profile: "{self.code_profile}"  # low (0.5B), high (1.5B)
ollama_host: "{self.ollama_host}"

# Default Search Behavior
default_limit: {self.default_limit}
default_hybrid: {str(self.default_hybrid).lower()}  # Combine vector + BM25

# HyDE (Hypothetical Document Embeddings)
# Generates a hypothetical answer and embeds that instead of the query.
# Best for knowledge-seeking questions. Adds ~100-500ms latency.
#
# Backends:
#   - claude_sdk: Uses Claude Code Agent SDK (default, best with Claude agents)
#   - ollama: Uses local Ollama models (fallback for standalone use)
hyde:
  enabled: {str(self.hyde.enabled).lower()}
  backend: "{self.hyde.backend}"  # claude_sdk (default) or ollama
  claude_model: "{self.hyde.claude_model}"  # haiku (fast), sonnet, opus
  ollama_model: "{self.hyde.ollama_model}"  # Ollama model (when backend: ollama)
  max_tokens: {self.hyde.max_tokens}

# Cross-Encoder Reranking
# Retrieves more candidates, then reranks with a cross-encoder.
# Significantly improves precision. Adds ~50-200ms (GPU) or ~500ms (CPU).
reranker:
  enabled: {str(self.reranker.enabled).lower()}
  model: "{self.reranker.model}"
  top_k: {self.reranker.top_k}  # Retrieve this many candidates
  top_n: {self.reranker.top_n}  # Return this many after reranking
  device: "{self.reranker.device}"  # auto, cuda, or cpu

# Query Expansion
# Expands query with related terms for better recall.
#
# Backends:
#   - claude_sdk: Uses Claude Code Agent SDK (default)
#   - ollama: Uses local Ollama models (fallback)
query_expansion:
  enabled: {str(self.query_expansion.enabled).lower()}
  backend: "{self.query_expansion.backend}"  # claude_sdk (default) or ollama
  claude_model: "{self.query_expansion.claude_model}"  # haiku, sonnet, opus
  ollama_model: "{self.query_expansion.ollama_model}"  # Ollama model (fallback)

# Parent Document Expansion
# After retrieving chunks, expand to their parent documents.
expand_parents: {str(self.expand_parents).lower()}
"""
        path.write_text(content)


# Global config cache
_config: RAGConfig | None = None
_config_path: Path | None = None


def load_rag_config(path: Path | None = None) -> RAGConfig:
    """Load or return cached RAG configuration.

    Searches for config in order:
    1. Explicitly provided path
    2. ./rag_config.yaml
    3. ./configs/rag.yaml
    4. Default config

    Args:
        path: Optional explicit config path

    Returns:
        RAGConfig instance
    """
    global _config, _config_path

    # Return cached if same path
    if _config is not None and (path is None or path == _config_path):
        return _config

    # Search for config
    search_paths = [
        Path("./rag_config.yaml"),
        Path("./configs/rag.yaml"),
    ]
    if path:
        search_paths.insert(0, path)

    for p in search_paths:
        if p.exists():
            _config = RAGConfig.from_yaml(p)
            _config_path = p
            return _config

    # Use defaults
    _config = RAGConfig()
    _config_path = None
    return _config


def reset_config_cache() -> None:
    """Reset the config cache. Useful for testing."""
    global _config, _config_path
    _config = None
    _config_path = None
