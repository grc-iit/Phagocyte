"""Configuration management using Pydantic."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ChunkingConfig(BaseModel):
    """Chunking configuration per content type.

    Note: We use structure-aware chunking which provides better semantic
    boundaries than character-based overlap:
    - Code: tree-sitter AST parsing (respects function/class boundaries)
    - Text/Papers: header-aware parsing (respects section boundaries)
    """

    # Code chunking - AST-aware via tree-sitter
    code_chunk_size: int = Field(default=1024, description="Token size for code chunks")

    # Paper chunking - header-aware
    paper_chunk_size: int = Field(default=2048, description="Token size for paper chunks")

    # Website/markdown chunking - header-aware
    markdown_chunk_size: int = Field(default=1024, description="Token size for markdown chunks")


class EmbeddingConfig(BaseModel):
    """Embedding generation configuration."""

    # Backend selection: ollama (default) or transformers
    backend: str = Field(
        default="ollama",
        description="Embedding backend: ollama (default), transformers",
    )

    # Model profile selection
    text_profile: str = Field(
        default="low", description="Text embedding profile: low, medium, high"
    )
    code_profile: str = Field(
        default="low", description="Code embedding profile: low, high"
    )
    multimodal_profile: str = Field(
        default="low", description="Multimodal embedding profile: low, high"
    )

    # Ollama server URL
    ollama_host: str = Field(
        default="http://localhost:11434", description="Ollama server URL"
    )

    # Transformers-specific settings
    torch_device: str = Field(default="auto", description="Torch device: auto, cuda, cpu")
    torch_dtype: str = Field(default="bfloat16", description="Torch dtype: float32, float16, bfloat16")
    use_flash_attention: bool = Field(default=True, description="Use flash attention if available")

    # Batch processing
    batch_size: int = Field(default=32, description="Batch size for embedding")
    max_concurrent: int = Field(default=4, description="Max concurrent embedding requests")

    # Retry configuration
    max_retries: int = Field(default=3, description="Max retries on failure")
    retry_delay: float = Field(default=1.0, description="Delay between retries in seconds")


class DatabaseConfig(BaseModel):
    """LanceDB configuration."""

    # Connection
    uri: str = Field(default="./lancedb", description="LanceDB database path")

    # Table mode
    table_mode: str = Field(
        default="separate", description="Table mode: separate, unified, both"
    )

    # Table names
    text_table: str = Field(default="text_chunks", description="Table for text/paper chunks")
    code_table: str = Field(default="code_chunks", description="Table for code chunks")
    image_table: str = Field(default="image_chunks", description="Table for image chunks")
    unified_table: str = Field(default="chunks", description="Unified table name")

    # Indexing
    create_vector_index: bool = Field(default=True, description="Create IVF-PQ index")
    create_fts_index: bool = Field(default=True, description="Create full-text search index")
    ivf_partitions: int = Field(default=256, description="IVF partitions for vector index")


class ProcessingConfig(BaseModel):
    """Processing pipeline configuration."""

    # Input/output
    input_dir: Path = Field(default=Path("./input"), description="Input directory")

    # Incremental processing
    incremental: bool = Field(default=True, description="Skip unchanged files")
    state_file: Path = Field(
        default=Path(".processor_state.json"), description="State file path"
    )

    # Concurrency
    max_concurrent_files: int = Field(default=5, description="Max files to process concurrently")


class ContentMappingConfig(BaseModel):
    """Content type mapping from directory names."""

    codebases: str = Field(default="code", description="Chunker for codebases directory")
    papers: str = Field(default="paper", description="Chunker for papers directory")
    websites: str = Field(default="markdown", description="Chunker for websites directory")
    books: str = Field(default="paper", description="Chunker for books directory")
    youtube: str = Field(default="markdown", description="Chunker for youtube directory")


class ProcessorConfig(BaseModel):
    """Main configuration for the processor."""

    content_mapping: ContentMappingConfig = Field(default_factory=ContentMappingConfig)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    verbose: bool = Field(default=False, description="Verbose output")

    @classmethod
    def from_yaml(cls, path: Path) -> "ProcessorConfig":
        """Load configuration from YAML file."""
        if not path.exists():
            return cls()

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(**data) if data else cls()

    def to_yaml(self, path: Path) -> None:
        """Save configuration to YAML file."""
        with open(path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False, sort_keys=False)

    def merge_cli_args(self, **kwargs: Any) -> "ProcessorConfig":
        """Merge CLI arguments into config (CLI takes precedence)."""
        data = self.model_dump()

        # Map CLI args to nested config structure
        cli_mappings = {
            "output": ("database", "uri"),
            "embedder": ("embedding", "backend"),
            "text_profile": ("embedding", "text_profile"),
            "code_profile": ("embedding", "code_profile"),
            "multimodal_profile": ("embedding", "multimodal_profile"),
            "ollama_host": ("embedding", "ollama_host"),
            "torch_device": ("embedding", "torch_device"),
            "batch_size": ("embedding", "batch_size"),
            "table_mode": ("database", "table_mode"),
            "incremental": ("processing", "incremental"),
            "verbose": ("verbose",),
        }

        for cli_key, config_path in cli_mappings.items():
            if cli_key in kwargs and kwargs[cli_key] is not None:
                if len(config_path) == 1:
                    data[config_path[0]] = kwargs[cli_key]
                else:
                    section, key = config_path
                    if section not in data:
                        data[section] = {}
                    data[section][key] = kwargs[cli_key]

        return ProcessorConfig(**data)


def load_config(config_path: Path | None = None) -> ProcessorConfig:
    """Load configuration from file or return defaults.

    Search order:
    1. Explicit path (if provided)
    2. ./processor.yaml
    3. ./configs/default.yaml
    4. Defaults
    """
    if config_path and config_path.exists():
        return ProcessorConfig.from_yaml(config_path)

    # Search for config files
    search_paths = [
        Path("./processor.yaml"),
        Path("./configs/default.yaml"),
    ]

    for path in search_paths:
        if path.exists():
            return ProcessorConfig.from_yaml(path)

    return ProcessorConfig()
