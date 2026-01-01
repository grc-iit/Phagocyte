"""RAG retrieval-time optimizations.

This package contains modules for improving RAG retrieval quality:

- hyde: HyDE (Hypothetical Document Embeddings) query transformation
- reranker: Cross-encoder reranking for improved precision
- parent_expansion: Expand to parent documents for broader context

These optimizations add latency but can significantly improve
retrieval quality for certain query types.
"""

from .hyde import hyde_transform
from .parent_expansion import expand_to_parents
from .reranker import rerank_results

__all__ = ["hyde_transform", "rerank_results", "expand_to_parents"]
