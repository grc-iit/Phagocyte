"""Agent-based reference parsing module.

This module provides AI agent implementations for parsing references
from research documents using:
- Anthropic Claude (via anthropic SDK)
- Google Gemini (via google-adk)
"""

from .base import AgentParser, AgentParseResult
from .factory import create_agent, list_available_agents, is_agent_available

__all__ = [
    "AgentParser",
    "AgentParseResult", 
    "create_agent",
    "list_available_agents",
    "is_agent_available",
]
