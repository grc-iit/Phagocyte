"""Cross-encoder reranking for improved precision.

Reranking uses a cross-encoder model to score query-document pairs
more accurately than bi-encoder similarity. The process:

1. Retrieve more candidates than needed (e.g., 20 instead of 5)
2. Score each (query, document) pair with cross-encoder
3. Return top-N by cross-encoder score

This significantly improves precision but adds latency:
- GPU: ~50-200ms for 20 candidates
- CPU: ~500ms+ for 20 candidates

Best for: High-precision requirements, final ranking
Models: BAAI/bge-reranker-v2-m3 (recommended), ms-marco-MiniLM-L-6-v2

Reference: https://www.sbert.net/docs/cross_encoder/cross_encoder_usage.html
"""

from typing import Any

from ..config import RAGConfig

# Global reranker cache (lazy loaded)
_reranker: Any | None = None
_reranker_model: str | None = None


def _get_reranker(config: RAGConfig):
    """Lazy load cross-encoder model.

    The model is cached globally to avoid reloading on every request.

    Args:
        config: RAG configuration with reranker settings

    Returns:
        CrossEncoder instance
    """
    global _reranker, _reranker_model

    # Return cached if same model
    if _reranker is not None and _reranker_model == config.reranker.model:
        return _reranker

    try:
        from sentence_transformers import CrossEncoder
    except ImportError:
        raise ImportError(
            "Reranking requires sentence-transformers. "
            "Install with: uv sync --extra reranker"
        )

    # Determine device
    device = config.reranker.device
    if device == "auto":
        try:
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"

    _reranker = CrossEncoder(config.reranker.model, device=device)
    _reranker_model = config.reranker.model

    return _reranker


async def rerank_results(
    query: str,
    candidates: list[dict],
    top_n: int,
    config: RAGConfig,
) -> list[dict]:
    """Rerank candidates using cross-encoder.

    Scores each query-document pair and returns the top-N by
    cross-encoder score.

    Args:
        query: Original query
        candidates: List of candidate documents (must have 'content' key)
        top_n: Number of results to return
        config: RAG configuration with reranker settings

    Returns:
        Reranked and filtered results with added _rerank_score
    """
    if not candidates:
        return []

    if not config.reranker.enabled and len(candidates) <= top_n:
        return candidates[:top_n]

    reranker = _get_reranker(config)

    # Prepare query-document pairs
    pairs = [[query, doc.get("content", "")] for doc in candidates]

    # Get reranking scores (sync operation, but fast)
    scores = reranker.predict(pairs)

    # Combine with original documents
    scored = list(zip(candidates, scores))

    # Sort by reranking score (higher is better)
    scored.sort(key=lambda x: x[1], reverse=True)

    # Add rerank score and return top_n
    results = []
    for doc, score in scored[:top_n]:
        doc = doc.copy()  # Don't modify original
        doc["_rerank_score"] = float(score)
        results.append(doc)

    return results


def clear_reranker_cache() -> None:
    """Clear the reranker model cache.

    Useful for testing or when switching models.
    """
    global _reranker, _reranker_model
    _reranker = None
    _reranker_model = None
