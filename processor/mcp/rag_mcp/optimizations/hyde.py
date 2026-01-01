"""HyDE (Hypothetical Document Embeddings) query transformation.

HyDE improves retrieval by generating a hypothetical answer to the query
and embedding that instead of the raw query. This works because:

1. User queries are often short and lack context
2. A hypothetical answer is more similar to actual documents
3. The embedding of the answer is closer to relevant documents

Supports two backends:
- claude_sdk: Uses Claude Code Agent SDK (default, best when used with Claude agents)
- ollama: Uses local Ollama models (fallback for standalone use)

Best for: Knowledge-seeking questions, conceptual queries
Latency: +100-500ms (one LLM generation)

Reference: https://arxiv.org/abs/2212.10496
"""

import httpx

from ..config import RAGConfig


async def _hyde_via_claude_sdk(query: str, config: RAGConfig) -> str:
    """Generate hypothetical document using Claude Code Agent SDK.

    Uses the claude-agent-sdk query() function for a one-off generation.
    This is the preferred method when running within a Claude agent context.

    Args:
        query: Original user query
        config: RAG configuration with HyDE settings

    Returns:
        Hypothetical document text
    """
    try:
        from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock
        from claude_agent_sdk import query as claude_query
    except ImportError:
        raise ImportError(
            "Claude Agent SDK not available. "
            "Install with: pip install claude-agent-sdk "
            "Or set hyde.backend to 'ollama' in config."
        )

    prompt = config.hyde.prompt_template.format(query=query)

    options = ClaudeAgentOptions(
        model=config.hyde.claude_model,
        max_turns=1,
        allowed_tools=[],  # No tools needed for simple generation
    )

    hypothetical = ""
    try:
        async for message in claude_query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        hypothetical += block.text
            elif isinstance(message, ResultMessage):
                break

        if hypothetical.strip():
            return hypothetical.strip()
        return query

    except Exception:
        # On error, fall back to original query
        return query


async def _hyde_via_ollama(query: str, config: RAGConfig) -> str:
    """Generate hypothetical document using Ollama.

    Fallback method for standalone use without Claude agent context.

    Args:
        query: Original user query
        config: RAG configuration with HyDE settings

    Returns:
        Hypothetical document text
    """
    prompt = config.hyde.prompt_template.format(query=query)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{config.ollama_host}/api/generate",
                json={
                    "model": config.hyde.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": config.hyde.max_tokens},
                },
            )
            response.raise_for_status()
            data = response.json()
            hypothetical = data.get("response", "").strip()

            if hypothetical:
                return hypothetical
            return query

    except Exception:
        # On error, fall back to original query
        return query


async def hyde_transform(query: str, config: RAGConfig) -> str:
    """Generate a hypothetical document for the query.

    Instead of embedding the raw query, we generate what an ideal
    answer might look like and return that for embedding.

    Uses the configured backend:
    - claude_sdk: Uses Claude Code Agent SDK (default)
    - ollama: Uses local Ollama models

    Args:
        query: Original user query
        config: RAG configuration with HyDE settings

    Returns:
        Hypothetical document text to embed instead of query
    """
    if not config.hyde.enabled and not query:
        return query

    backend = config.hyde.backend.lower()

    if backend == "claude_sdk":
        try:
            return await _hyde_via_claude_sdk(query, config)
        except ImportError:
            # Fall back to Ollama if Claude SDK not available
            return await _hyde_via_ollama(query, config)
    elif backend == "ollama":
        return await _hyde_via_ollama(query, config)
    else:
        # Unknown backend, try Claude SDK first, then Ollama
        try:
            return await _hyde_via_claude_sdk(query, config)
        except ImportError:
            return await _hyde_via_ollama(query, config)


async def hyde_transform_batch(queries: list[str], config: RAGConfig) -> list[str]:
    """Transform multiple queries using HyDE.

    Args:
        queries: List of original queries
        config: RAG configuration

    Returns:
        List of hypothetical documents (same order as input)
    """
    import asyncio

    tasks = [hyde_transform(q, config) for q in queries]
    return await asyncio.gather(*tasks)
