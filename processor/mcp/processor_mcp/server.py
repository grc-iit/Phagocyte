"""MCP Server for document processing operations.

This server exposes tools for:
- Processing files/directories into LanceDB vector database
- Checking embedding service availability
- Managing embedding model setup
- Database statistics and export/import

Usage:
    uv run processor-mcp
"""

from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize MCP server
mcp = FastMCP(
    name="processor-mcp",
    instructions="""
Document Processing MCP Server

Provides tools for processing documents into a RAG-ready LanceDB vector database.

Before processing, ensure:
1. Ollama is running (ollama serve)
2. Required models are available (use setup_models tool or run: uv run processor setup)

Workflow:
1. check_services - Verify backends are available
2. setup_models - Download embedding models if needed
3. process_documents - Process files into LanceDB
4. get_db_stats - Verify results

Key concepts:
- Embedder: 'ollama' (default, fast) or 'transformers' (GPU-accelerated)
- Profiles: Control quality vs speed tradeoff
  - text: low (0.6B), medium (4B), high (8B)
  - code: low (0.5B), high (1.5B)
- Table modes: 'separate' (text/code/image tables), 'unified' (single table), 'both'
- Incremental: Skip unchanged files (default True)
"""
)


# =============================================================================
# Tool Input/Output Models
# =============================================================================


class ProcessInput(BaseModel):
    """Input for document processing."""

    input_path: str = Field(description="File or directory to process")
    output_db: str = Field(default="./lancedb", description="LanceDB output path")
    embedder: Literal["ollama", "transformers"] = Field(
        default="ollama", description="Embedding backend"
    )
    text_profile: Literal["low", "medium", "high"] = Field(
        default="low", description="Text embedding quality (low=fast, high=best)"
    )
    code_profile: Literal["low", "high"] = Field(
        default="low", description="Code embedding quality"
    )
    table_mode: Literal["separate", "unified", "both"] = Field(
        default="separate", description="How to organize database tables"
    )
    batch_size: int = Field(default=32, ge=1, le=256, description="Embedding batch size")
    incremental: bool = Field(default=True, description="Skip unchanged files")
    content_type: Literal["auto", "code", "paper", "markdown"] = Field(
        default="auto", description="Force content type detection"
    )


class ProcessResult(BaseModel):
    """Result of processing operation."""

    files_processed: int
    chunks_created: int
    images_processed: int
    errors: int
    output_path: str


class ServiceStatus(BaseModel):
    """Status of embedding services."""

    ollama_cli: bool
    ollama_server: bool
    available_models: list[str]
    transformers_available: bool
    openclip_available: bool


class DbStats(BaseModel):
    """Database statistics."""

    path: str
    tables: dict[str, dict]


class ExportResult(BaseModel):
    """Result of export operation."""

    format: str
    tables: dict[str, int]
    total_rows: int
    output_path: str


class SetupResult(BaseModel):
    """Result of model setup."""

    results: dict[str, dict]


# =============================================================================
# Tools
# =============================================================================


@mcp.tool()
async def process_documents(input: ProcessInput) -> ProcessResult:
    """Process documents through chunking, embedding, and loading into LanceDB.

    This is the main processing pipeline. It will:
    1. Discover files in input_path
    2. Detect content type (code, paper, markdown)
    3. Chunk using AST-aware (code) or header-aware (text) strategies
    4. Generate embeddings using the selected backend
    5. Load into LanceDB with vector indices

    Args:
        input: Processing configuration

    Returns:
        Statistics about processed files and chunks

    Example:
        process_documents(input_path="./my-codebase", output_db="./db", content_type="code")
    """
    from processor.config import load_config
    from processor.pipeline.processor import Pipeline

    # Load and configure
    config = load_config()
    config = config.merge_cli_args(
        output=input.output_db,
        embedder=input.embedder,
        text_profile=input.text_profile,
        code_profile=input.code_profile,
        table_mode=input.table_mode,
        batch_size=input.batch_size,
        incremental=input.incremental,
    )

    # Run pipeline
    pipeline = Pipeline(config)
    result = await pipeline.process(Path(input.input_path), content_type=input.content_type)

    return ProcessResult(
        files_processed=result.get("files_processed", 0),
        chunks_created=result.get("chunks_created", 0),
        images_processed=result.get("images_processed", 0),
        errors=result.get("errors", 0),
        output_path=input.output_db,
    )


@mcp.tool()
async def check_services(ollama_host: str = "http://localhost:11434") -> ServiceStatus:
    """Check availability of embedding backends.

    Verifies:
    - Ollama CLI is installed
    - Ollama server is running and accessible
    - Which embedding models are available
    - Whether optional backends (transformers, openclip) are installed

    Args:
        ollama_host: Ollama server URL

    Returns:
        Status of all embedding services
    """
    from processor.embedders.ollama import OllamaEmbedder

    status = ServiceStatus(
        ollama_cli=OllamaEmbedder.is_cli_available(),
        ollama_server=False,
        available_models=[],
        transformers_available=False,
        openclip_available=False,
    )

    # Check Ollama server
    embedder = OllamaEmbedder(host=ollama_host)
    status.ollama_server = await embedder.is_available()
    if status.ollama_server:
        status.available_models = await embedder.list_models()
    await embedder.close()

    # Check optional backends
    try:
        import sentence_transformers  # noqa: F401

        status.transformers_available = True
    except ImportError:
        pass

    try:
        import open_clip  # noqa: F401

        status.openclip_available = True
    except ImportError:
        pass

    return status


@mcp.tool()
async def setup_models(
    minimal: bool = True,
    ollama_host: str = "http://localhost:11434",
) -> SetupResult:
    """Download required embedding models via Ollama.

    Downloads embedding models needed for processing. By default only
    downloads the minimal set for fast setup.

    Args:
        minimal: If True, only download qwen3-embedding:0.6b (text).
                 If False, also download jina-code-embeddings models.
        ollama_host: Ollama server URL

    Returns:
        Download status for each model
    """
    from processor.embedders.ollama import OllamaEmbedder

    models = [("qwen3-embedding:0.6b", "text-low")]
    if not minimal:
        models.extend(
            [
                ("hf.co/jinaai/jina-code-embeddings-0.5b-GGUF:Q8_0", "code-low"),
                ("hf.co/jinaai/jina-code-embeddings-1.5b-GGUF:Q8_0", "code-high"),
            ]
        )

    results = {}
    for model_name, profile in models:
        success, msg = OllamaEmbedder.pull_model(model_name)
        results[profile] = {
            "model": model_name,
            "success": success,
            "message": msg[:200] if msg else "",
        }

    return SetupResult(results=results)


@mcp.tool()
async def get_db_stats(
    db_path: str,
    table: str | None = None,
) -> DbStats:
    """Get statistics for a LanceDB database.

    Shows table names, row counts, and column schemas. Useful for
    verifying processing results.

    Args:
        db_path: Path to LanceDB database
        table: Optional specific table to inspect

    Returns:
        Database statistics
    """
    import lancedb

    if not Path(db_path).exists():
        raise ValueError(f"Database not found at {db_path}")

    db = lancedb.connect(db_path)
    table_names = db.table_names() if table is None else [table]

    stats = {}
    for table_name in table_names:
        if table_name not in db.table_names():
            continue
        tbl = db.open_table(table_name)
        stats[table_name] = {
            "row_count": tbl.count_rows(),
            "columns": [f.name for f in tbl.schema],
        }

    return DbStats(path=db_path, tables=stats)


@mcp.tool()
async def export_db(
    db_path: str,
    output_path: str,
    format: Literal["lance", "csv"] = "lance",
    include_vectors: bool = False,
    tables: list[str] | None = None,
) -> ExportResult:
    """Export database to a portable format.

    Exports the LanceDB database for sharing or backup. The 'lance' format
    preserves full fidelity including vectors. The 'csv' format is for
    inspection but loses vector data by default.

    Args:
        db_path: Source database path
        output_path: Output directory
        format: Export format ('lance' or 'csv')
        include_vectors: Include vector columns in CSV (very large!)
        tables: Specific tables to export (None = all)

    Returns:
        Export statistics
    """
    from processor.database.exporter import DatabaseExporter

    exporter = DatabaseExporter(db_path)

    if format == "lance":
        result = exporter.export_to_lance(Path(output_path), tables=tables)
    else:
        result = exporter.export_to_csv(
            Path(output_path), include_vectors=include_vectors, tables=tables
        )

    exporter.export_manifest(Path(output_path), format, result)

    return ExportResult(
        format=format,
        tables=result,
        total_rows=sum(result.values()),
        output_path=output_path,
    )


@mcp.tool()
async def import_db(
    export_path: str,
    output_path: str,
    tables: list[str] | None = None,
) -> dict:
    """Import database from a Lance export.

    Restores a database from a previous export. Only works with
    'lance' format exports (not CSV).

    Args:
        export_path: Path to exported Lance directory
        output_path: Target database path
        tables: Specific tables to import (None = all)

    Returns:
        Import statistics
    """
    from processor.database.exporter import DatabaseImporter

    importer = DatabaseImporter(output_path)
    result = importer.import_from_lance(Path(export_path), tables=tables)

    return {"imported_tables": result, "output_path": output_path}


# =============================================================================
# Entry Point
# =============================================================================


def main():
    """Entry point for processor-mcp."""
    mcp.run()


if __name__ == "__main__":
    main()
