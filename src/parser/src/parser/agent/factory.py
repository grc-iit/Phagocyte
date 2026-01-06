"""Factory for creating agent instances."""

import importlib.util
from typing import Literal

from .base import AgentParser

AgentType = Literal["anthropic", "gemini", "claude", "google"]


def create_agent(
    agent_type: AgentType,
    api_key: str | None = None,
    model: str | None = None,
) -> AgentParser:
    """Create an agent instance.

    Args:
        agent_type: Type of agent:
            - 'claude': Claude via claude-agent-sdk (NO API key needed - uses Claude Code CLI)
            - 'anthropic': Claude via direct Anthropic API (requires ANTHROPIC_API_KEY)
            - 'gemini': Gemini via Google ADK (requires GOOGLE_API_KEY)
            - 'google': Gemini via google-generativeai (requires GOOGLE_API_KEY)
        api_key: API key for the service (not needed for claude)
        model: Model to use (uses default if not specified)

    Returns:
        AgentParser instance

    Raises:
        ValueError: If agent_type is not supported
    """
    # Normalize agent type names
    agent_type_lower = agent_type.lower()

    if agent_type_lower == "claude":
        # Use claude-agent-sdk (no API key needed - uses Claude Code CLI)
        from .anthropic_agent import AnthropicAgent
        return AnthropicAgent(api_key=api_key, model=model, use_agent_sdk=True)

    elif agent_type_lower == "anthropic":
        # Use Anthropic API directly (requires ANTHROPIC_API_KEY)
        from .anthropic_agent import AnthropicAgent
        return AnthropicAgent(api_key=api_key, model=model, use_agent_sdk=False)

    elif agent_type_lower == "gemini":
        # Use google-adk (Agent Development Kit)
        from .gemini_agent import GeminiAgent
        return GeminiAgent(api_key=api_key, model=model, use_adk=True)

    elif agent_type_lower == "google":
        # Use google-generativeai API directly (requires GOOGLE_API_KEY)
        from .gemini_agent import GeminiAgent
        return GeminiAgent(api_key=api_key, model=model, use_adk=False)

    else:
        raise ValueError(
            f"Unsupported agent type: {agent_type}. "
            f"Supported types: claude, anthropic, gemini, google"
        )


def list_available_agents() -> list[dict]:
    """List available agent types with their details.

    Returns:
        List of agent info dictionaries
    """
    return [
        {
            "type": "claude",
            "aliases": [],
            "description": "Claude via claude-agent-sdk (NO API key needed - uses Claude Code CLI)",
            "env_var": None,
            "default_model": "claude-sonnet-4-20250514",
            "package": "claude-agent-sdk",
        },
        {
            "type": "anthropic",
            "aliases": [],
            "description": "Claude via direct Anthropic API (requires ANTHROPIC_API_KEY)",
            "env_var": "ANTHROPIC_API_KEY",
            "default_model": "claude-sonnet-4-20250514",
            "package": "anthropic",
        },
        {
            "type": "gemini",
            "aliases": [],
            "description": "Gemini via Google ADK (requires GOOGLE_API_KEY)",
            "env_var": "GOOGLE_API_KEY",
            "default_model": "gemini-2.0-flash",
            "package": "google-adk",
        },
        {
            "type": "google",
            "aliases": [],
            "description": "Gemini via google-genai (requires GOOGLE_API_KEY)",
            "env_var": "GOOGLE_API_KEY",
            "default_model": "gemini-2.0-flash",
            "package": "google-genai",
        },
    ]


def is_agent_available(agent_type: AgentType) -> tuple[bool, str]:
    """Check if an agent type is available (package installed).

    Args:
        agent_type: Type of agent to check

    Returns:
        Tuple of (available, message)
    """
    agent_type_lower = agent_type.lower()

    if agent_type_lower == "claude":
        spec = importlib.util.find_spec("claude_agent_sdk")
        if spec is not None:
            return True, "claude-agent-sdk package installed (no API key needed)"
        return False, "claude-agent-sdk package not installed. Install with: pip install claude-agent-sdk"

    elif agent_type_lower == "anthropic":
        spec = importlib.util.find_spec("anthropic")
        if spec is not None:
            return True, "anthropic package installed (requires ANTHROPIC_API_KEY)"
        return False, "anthropic package not installed. Install with: pip install anthropic"

    elif agent_type_lower == "gemini":
        spec = importlib.util.find_spec("google.adk.agents")
        if spec is not None:
            return True, "google-adk package installed"
        return False, "google-adk package not installed. Install with: pip install google-adk"

    elif agent_type_lower == "google":
        spec = importlib.util.find_spec("google.genai")
        if spec is not None:
            return True, "google-genai package installed (requires GOOGLE_API_KEY)"
        return False, "google-genai package not installed. Install with: pip install google-genai"

    return False, f"Unknown agent type: {agent_type}"
