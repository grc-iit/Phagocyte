"""Processor MCP Server.

Exposes document processing operations as MCP tools for AI agents.

Usage:
    uv run processor-mcp
"""

from .server import main, mcp

__all__ = ["main", "mcp"]
