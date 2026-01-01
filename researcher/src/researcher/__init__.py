"""Researcher module for programmatic deep research using Gemini API.

This module provides automated research capabilities using Google's
Gemini Deep Research Agent to conduct multi-step research tasks and
produce detailed, cited reports.

Example:
    from researcher import DeepResearcher, ResearchConfig
    
    researcher = DeepResearcher()
    result = await researcher.research("What are the latest advances in quantum computing?")
    print(result.report)
"""

from .deep_research import (
    DeepResearcher,
    ResearchConfig,
    ResearchMode,
    ResearchResult,
    ResearchStatus,
    deep_research,
)

__all__ = [
    "DeepResearcher",
    "ResearchConfig",
    "ResearchMode",
    "ResearchResult",
    "ResearchStatus",
    "deep_research",
]
