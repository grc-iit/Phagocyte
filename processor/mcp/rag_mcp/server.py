"""MCP Server for RAG database search operations.

This server provides semantic search over processed document databases
with optional retrieval-time optimizations.

Features:
- Vector search (fast, default)
- Hybrid search (vector + BM25 with RRF fusion)
- HyDE query transformation
- Cross-encoder reranking
- Parent document expansion

Usage:
    uv run rag-mcp                    # Start server
    uv run rag-mcp --config_generate  # Generate config template
"""

import sys
import time
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from .config import RAGConfig, load_rag_config

# Initialize MCP server
mcp = FastMCP(
    name="rag-mcp",
    instructions="""
RAG Search MCP Server

Provides semantic search over LanceDB vector databases created by processor-mcp.

Available optimizations (can be combined):
- hybrid: Combine vector + BM25 keyword search with RRF fusion (+10-30ms)
- use_hyde: Generate hypothetical answer, embed that instead of query (+200-500ms)
- rerank: Retrieve more candidates, rerank with cross-encoder (+50-200ms GPU)
- expand_parents: Deduplicate by parent document, return broader context (+5-20ms)

Recommended combinations:
- Fast search: No optimizations (default)
- Better recall: hybrid=True
- Knowledge questions: use_hyde=True, rerank=True
- Code search: hybrid=True (keywords often important in code)
- Maximum precision: hybrid=True, use_hyde=True, rerank=True

Important: The embedding profiles must match the processor config used
to build the database, or search results will be poor.
"""
)


# =============================================================================
# Tool Input/Output Models
# =============================================================================


class SearchInput(BaseModel):
    """Input for search operation."""

    query: str = Field(description="Search query")
    db_path: str = Field(default="./lancedb", description="LanceDB database path")
    table: Literal["text_chunks", "code_chunks", "chunks", "image_chunks"] = Field(
        default="text_chunks", description="Table to search"
    )
    limit: int = Field(default=5, ge=1, le=100, description="Number of results")

    # Optimization flags
    hybrid: bool = Field(
        default=False, description="Use hybrid search (vector + BM25)"
    )
    use_hyde: bool = Field(
        default=False, description="Use HyDE query transformation"
    )
    rerank: bool = Field(
        default=False, description="Rerank results with cross-encoder"
    )
    rerank_top_k: int = Field(
        default=20, ge=5, le=100, description="Candidates for reranking"
    )
    expand_parents: bool = Field(
        default=False, description="Expand to parent documents"
    )


class SearchResult(BaseModel):
    """Single search result."""

    content: str
    source_file: str
    score: float
    chunk_id: str
    metadata: dict = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Search response with results and metadata."""

    results: list[SearchResult]
    query: str
    optimizations_used: list[str]
    total_time_ms: float


class ImageSearchResult(BaseModel):
    """Image search result."""

    figure_id: str
    caption: str
    vlm_description: str
    image_path: str
    source_paper: str
    score: float


class TableInfo(BaseModel):
    """Table information."""

    name: str
    row_count: int
    searchable: bool


class ListTablesResponse(BaseModel):
    """Response from list_tables."""

    db_path: str
    tables: dict[str, TableInfo]


# =============================================================================
# Tools
# =============================================================================


@mcp.tool()
async def search(input: SearchInput) -> SearchResponse:
    """Search the RAG database for relevant documents.

    Performs semantic search over the processed document database.
    Supports various optimizations that can be enabled individually
    or combined for better results at the cost of latency.

    Args:
        input: Search configuration including query and optimization flags

    Returns:
        Ranked search results with metadata

    Example:
        search(query="how does caching work", hybrid=True, limit=10)
    """
    import lancedb

    from processor.embedders.ollama import OllamaEmbedder
    from processor.embedders.profiles import EmbedderBackend, get_model_for_profile

    start = time.time()
    optimizations_used = []

    config = load_rag_config()

    # Validate database exists
    if not Path(input.db_path).exists():
        raise ValueError(
            f"Database not found at {input.db_path}. "
            f"Create it with: uv run processor process ./input -o {input.db_path}"
        )

    # Get query text (potentially transformed)
    query_text = input.query

    # HyDE transformation
    if input.use_hyde:
        from .optimizations.hyde import hyde_transform

        query_text = await hyde_transform(input.query, config)
        optimizations_used.append("hyde")

    # Get embedder based on table type
    if input.table == "code_chunks":
        profile, backend = get_model_for_profile(
            "code", config.code_profile, EmbedderBackend.OLLAMA
        )
    else:
        profile, backend = get_model_for_profile(
            "text", config.text_profile, EmbedderBackend.OLLAMA
        )

    embedder = OllamaEmbedder(
        model=profile.ollama_model,
        host=config.ollama_host,
    )

    # Embed query
    query_embedding = await embedder.embed(query_text)
    await embedder.close()

    # Connect to database
    db = lancedb.connect(input.db_path)
    if input.table not in db.table_names():
        available = ", ".join(db.table_names())
        raise ValueError(
            f"Table '{input.table}' not found. Available tables: {available}"
        )

    table = db.open_table(input.table)

    # Determine search count (more if reranking)
    search_k = input.rerank_top_k if input.rerank else input.limit

    # Perform search
    if input.hybrid:
        # Hybrid search with RRF fusion
        try:
            results = (
                table.search(query_type="hybrid")
                .vector(query_embedding)
                .text(input.query)  # Use original query for BM25
                .limit(search_k)
                .to_list()
            )
            optimizations_used.append("hybrid_rrf")
        except Exception:
            # Fall back to vector-only if hybrid not supported
            results = table.search(query_embedding).limit(search_k).to_list()
    else:
        # Pure vector search
        results = table.search(query_embedding).limit(search_k).to_list()

    # Reranking
    if input.rerank and results:
        from .optimizations.reranker import rerank_results

        results = await rerank_results(input.query, results, input.limit, config)
        optimizations_used.append("cross_encoder_rerank")

    # Parent expansion
    if input.expand_parents and results:
        from .optimizations.parent_expansion import expand_to_parents

        results = await expand_to_parents(results, table)
        optimizations_used.append("parent_expansion")

    # Format results
    search_results = []
    for r in results[: input.limit]:
        # Convert distance to similarity score (0-1 range, higher is better)
        distance = r.get("_distance", 0)
        score = max(0, 1.0 - (distance / 2.0))  # Normalize L2 distance

        search_results.append(
            SearchResult(
                content=r.get("content", "")[:2000],  # Truncate for response size
                source_file=r.get("source_file", ""),
                score=round(score, 4),
                chunk_id=r.get("id", ""),
                metadata={
                    k: v
                    for k, v in r.items()
                    if k
                    not in [
                        "content",
                        "source_file",
                        "id",
                        "vector",
                        "_distance",
                        "_relevance_score",
                    ]
                    and v is not None
                },
            )
        )

    elapsed_ms = (time.time() - start) * 1000

    return SearchResponse(
        results=search_results,
        query=input.query,
        optimizations_used=optimizations_used,
        total_time_ms=round(elapsed_ms, 2),
    )


@mcp.tool()
async def search_images(
    query: str,
    db_path: str = "./lancedb",
    limit: int = 5,
) -> list[ImageSearchResult]:
    """Search for relevant images/figures.

    Searches the image_chunks table using text embeddings of VLM
    descriptions. Useful for finding figures, charts, and diagrams
    from processed papers.

    Args:
        query: Text description to search for
        db_path: LanceDB database path
        limit: Number of results

    Returns:
        Image results with captions and file paths
    """
    import lancedb

    from processor.embedders.ollama import OllamaEmbedder
    from processor.embedders.profiles import EmbedderBackend, get_model_for_profile

    config = load_rag_config()

    if not Path(db_path).exists():
        raise ValueError(f"Database not found at {db_path}")

    db = lancedb.connect(db_path)
    if "image_chunks" not in db.table_names():
        return []

    # Get text embedder for query
    profile, _ = get_model_for_profile(
        "text", config.text_profile, EmbedderBackend.OLLAMA
    )
    embedder = OllamaEmbedder(model=profile.ollama_model, host=config.ollama_host)
    query_embedding = await embedder.embed(query)
    await embedder.close()

    # Search text embeddings
    table = db.open_table("image_chunks")
    results = (
        table.search(query_embedding, vector_column_name="text_vector")
        .limit(limit)
        .to_list()
    )

    return [
        ImageSearchResult(
            figure_id=str(r.get("figure_id", "")),
            caption=r.get("caption", "") or "",
            vlm_description=(r.get("vlm_description", "") or "")[:500],
            image_path=r.get("image_path", "") or "",
            source_paper=r.get("source_paper", "") or "",
            score=round(1.0 - r.get("_distance", 0) / 2.0, 4),
        )
        for r in results
    ]


@mcp.tool()
async def list_tables(db_path: str = "./lancedb") -> ListTablesResponse:
    """List available tables in the RAG database.

    Shows all tables with their row counts. Excludes metadata tables
    (prefixed with _).

    Args:
        db_path: LanceDB database path

    Returns:
        Table information including searchable status
    """
    import lancedb

    if not Path(db_path).exists():
        raise ValueError(f"Database not found at {db_path}")

    db = lancedb.connect(db_path)
    tables = {}

    for name in db.table_names():
        if name.startswith("_"):
            continue  # Skip metadata tables
        table = db.open_table(name)
        tables[name] = TableInfo(
            name=name,
            row_count=table.count_rows(),
            searchable=True,
        )

    return ListTablesResponse(db_path=db_path, tables=tables)


@mcp.tool()
async def generate_config(output_path: str = "./rag_config.yaml") -> str:
    """Generate a template RAG configuration file.

    Creates a YAML config with all available options and sensible
    defaults. Edit this file to customize search behavior.

    Args:
        output_path: Where to write the config file

    Returns:
        Confirmation message
    """
    config = RAGConfig()
    path = Path(output_path)
    config.to_yaml(path)

    return f"Config template written to {output_path}"


# =============================================================================
# Entry Point
# =============================================================================


def main():
    """Entry point for rag-mcp."""
    # Handle --config_generate flag before MCP startup
    if "--config_generate" in sys.argv:
        config = RAGConfig()
        output = "rag_config.yaml"

        # Check for custom output path
        for i, arg in enumerate(sys.argv):
            if arg == "--config_generate" and i + 1 < len(sys.argv):
                next_arg = sys.argv[i + 1]
                if not next_arg.startswith("-"):
                    output = next_arg
                    break

        config.to_yaml(Path(output))
        print(f"Generated {output}")
        return

    # Handle --config flag to set config path
    config_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--config" and i + 1 < len(sys.argv):
            config_path = Path(sys.argv[i + 1])
            break

    if config_path:
        load_rag_config(config_path)

    mcp.run()


if __name__ == "__main__":
    main()
