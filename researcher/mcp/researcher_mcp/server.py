"""MCP Server for AI-powered deep research operations.

This server exposes tools for:
- Conducting deep research using Gemini API
- Different research modes (undirected, directed, no-research)
- Streaming research progress

Usage:
    uv run researcher-mcp
"""

import os
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize MCP server
mcp = FastMCP(
    name="researcher-mcp",
    instructions="""
Deep Research MCP Server

Provides AI-powered research capabilities using Google Gemini Deep Research API.

Before using, ensure:
1. GEMINI_API_KEY or GOOGLE_API_KEY environment variable is set
2. Get API key from: https://aistudio.google.com/

Research Modes:
- undirected: Web-first discovery (default) - searches broadly, good for exploration
- directed: Prioritize user-provided artifacts, web fills gaps - good for targeted research
- no-research: Analyze only provided materials, no web search - good for document analysis

Workflow:
1. deep_research - Conduct comprehensive research on a topic
2. Results are saved to output directory with:
   - research_report.md: Main report with citations
   - research_metadata.json: Query, timing, interaction info
   - thinking_steps.md: Agent reasoning (if verbose enabled)

Key concepts:
- Artifacts: URLs, file paths, or text content to include in research
- Output format: Custom formatting instructions for the report
- Max wait: Timeout for research completion (default 3600s = 1 hour)
"""
)


# =============================================================================
# Tool Input/Output Models
# =============================================================================


class ResearchInput(BaseModel):
    """Input for deep research operation."""

    query: str = Field(description="Research topic or question")
    output_dir: str = Field(default="./output", description="Output directory for results")
    mode: Literal["undirected", "directed", "no-research"] = Field(
        default="undirected",
        description="Research mode: undirected (web-first), directed (artifacts-first), no-research (artifacts only)"
    )
    artifacts: list[str] = Field(
        default_factory=list,
        description="Supporting materials: URLs, file paths, or text content"
    )
    output_format: str | None = Field(
        default=None,
        description="Custom output format instructions"
    )
    max_wait: int = Field(
        default=3600,
        ge=60,
        le=7200,
        description="Maximum wait time in seconds (default: 3600)"
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose output with thinking steps"
    )


class ResearchResult(BaseModel):
    """Result of research operation."""

    success: bool
    report_path: str | None = None
    metadata_path: str | None = None
    thinking_path: str | None = None
    query: str
    mode: str
    duration_seconds: float | None = None
    error: str | None = None


class ApiKeyStatus(BaseModel):
    """Status of API key configuration."""

    gemini_key_set: bool
    google_key_set: bool
    key_source: str | None


# =============================================================================
# Tools
# =============================================================================


@mcp.tool()
async def deep_research(input: ResearchInput) -> ResearchResult:
    """Conduct deep research on a topic using Gemini Deep Research API.

    Searches multiple sources, synthesizes findings, and produces a comprehensive
    report with structured citations (arXiv IDs, DOIs, GitHub URLs).

    Research Modes:
    - undirected: Web-first discovery, good for broad exploration
    - directed: Uses provided artifacts first, fills gaps with web search
    - no-research: Analyzes only provided materials, no external search

    Args:
        input: Research configuration including query, mode, and artifacts

    Returns:
        Paths to generated report and metadata files

    Example:
        deep_research(query="HDF5 file format best practices", mode="undirected")
        deep_research(query="Compare architectures", mode="directed", artifacts=["https://arxiv.org/..."])
    """
    import time
    from dotenv import load_dotenv
    
    load_dotenv()
    
    from researcher.deep_research import DeepResearcher, ResearchConfig, ResearchMode

    start_time = time.time()
    
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return ResearchResult(
            success=False,
            query=input.query,
            mode=input.mode,
            error="No API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable."
        )

    # Map mode string to enum
    mode_map = {
        "undirected": ResearchMode.UNDIRECTED,
        "directed": ResearchMode.DIRECTED,
        "no-research": ResearchMode.NO_RESEARCH,
    }
    research_mode = mode_map.get(input.mode, ResearchMode.UNDIRECTED)

    # Configure research
    config = ResearchConfig(
        output_format=input.output_format,
        max_wait_time=input.max_wait,
        enable_streaming=False,  # MCP doesn't support streaming well
        enable_thinking=input.verbose,
        mode=research_mode,
        artifacts=input.artifacts if input.artifacts else None,
    )

    try:
        researcher = DeepResearcher(api_key=api_key, config=config)
        output_path = Path(input.output_dir) / "research"
        output_path.mkdir(parents=True, exist_ok=True)

        # Conduct research
        result = await researcher.research(
            query=input.query,
            on_progress=None,  # No streaming for MCP
        )

        # Save the results to files
        result.save(output_path)

        duration = time.time() - start_time

        return ResearchResult(
            success=True,
            report_path=str(output_path / "research_report.md"),
            metadata_path=str(output_path / "research_metadata.json"),
            thinking_path=str(output_path / "thinking_steps.md") if result.thinking_steps else None,
            query=input.query,
            mode=input.mode,
            duration_seconds=round(duration, 2),
        )

    except Exception as e:
        return ResearchResult(
            success=False,
            query=input.query,
            mode=input.mode,
            error=str(e),
        )


@mcp.tool()
async def check_api_key() -> ApiKeyStatus:
    """Check if Gemini API key is configured.

    Checks for GEMINI_API_KEY or GOOGLE_API_KEY environment variables.

    Returns:
        Status of API key configuration
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    google_key = os.environ.get("GOOGLE_API_KEY")
    
    key_source = None
    if gemini_key:
        key_source = "GEMINI_API_KEY"
    elif google_key:
        key_source = "GOOGLE_API_KEY"
    
    return ApiKeyStatus(
        gemini_key_set=bool(gemini_key),
        google_key_set=bool(google_key),
        key_source=key_source,
    )


@mcp.tool()
async def list_research_outputs(output_dir: str = "./output") -> dict:
    """List research outputs in a directory.

    Scans the output directory for research results including
    reports, metadata, and thinking steps.

    Args:
        output_dir: Directory to scan for research outputs

    Returns:
        Dictionary with found outputs organized by research session
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        return {"error": f"Directory not found: {output_dir}", "sessions": []}
    
    sessions = []
    
    # Look for research subdirectory
    research_dir = output_path / "research"
    search_dirs = [research_dir, output_path] if research_dir.exists() else [output_path]
    
    for search_dir in search_dirs:
        # Find all report files
        for report_file in search_dir.glob("**/research_report.md"):
            session_dir = report_file.parent
            session = {
                "path": str(session_dir),
                "report": str(report_file) if report_file.exists() else None,
                "metadata": None,
                "thinking": None,
            }
            
            metadata_file = session_dir / "research_metadata.json"
            if metadata_file.exists():
                session["metadata"] = str(metadata_file)
                # Try to read query from metadata
                try:
                    import json
                    with open(metadata_file) as f:
                        meta = json.load(f)
                        session["query"] = meta.get("query", "Unknown")
                        session["timestamp"] = meta.get("timestamp", "Unknown")
                except Exception:
                    pass
            
            thinking_file = session_dir / "thinking_steps.md"
            if thinking_file.exists():
                session["thinking"] = str(thinking_file)
            
            sessions.append(session)
    
    return {
        "output_dir": str(output_path),
        "sessions": sessions,
        "total": len(sessions),
    }


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
