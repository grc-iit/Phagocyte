"""RAG MCP Server.

Exposes RAG search operations with retrieval-time optimizations as MCP tools.

Usage:
    uv run rag-mcp                    # Start server
    uv run rag-mcp --config_generate  # Generate config template
"""

from .config import RAGConfig, load_rag_config
from .server import main, mcp

__all__ = ["main", "mcp", "RAGConfig", "load_rag_config"]
