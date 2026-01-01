"""Parent document expansion for context retrieval.

When chunks are indexed with parent_id references, this module
expands retrieved chunks to their parent documents. This provides:

1. Broader context around the matched content
2. Deduplication when multiple chunks from same parent match
3. Better results for questions requiring full sections

The expansion process:
1. Group results by parent_id
2. Keep the best score per parent
3. Return deduplicated results sorted by score

Latency: +5-20ms (metadata lookup only)
"""

from typing import Any


async def expand_to_parents(
    results: list[dict],
    table: Any,
) -> list[dict]:
    """Expand retrieved chunks to their parent documents.

    Deduplicates by parent_id, keeping the best match score per parent.
    Results without parent_id are kept as-is.

    Args:
        results: List of retrieved chunks (with optional parent_id)
        table: LanceDB table for fetching parents (currently unused,
               but available for future parent content retrieval)

    Returns:
        Deduplicated results representing parent documents
    """
    if not results:
        return []

    # Track best score per parent/document
    best_scores: dict[str, float] = {}
    best_docs: dict[str, dict] = {}

    for r in results:
        parent_id = r.get("parent_id")
        doc_id = parent_id if parent_id else r.get("id", "")

        if not doc_id:
            continue

        # Use distance (lower is better) or relevance score (higher is better)
        distance = r.get("_distance", float("inf"))

        # Keep document with lowest distance (best match)
        if doc_id not in best_scores or distance < best_scores[doc_id]:
            best_scores[doc_id] = distance
            best_docs[doc_id] = r.copy()

    # Sort by score and return
    sorted_results = sorted(
        best_docs.values(), key=lambda x: x.get("_distance", float("inf"))
    )

    return sorted_results


async def expand_with_siblings(
    results: list[dict],
    table: Any,
    window: int = 1,
) -> list[dict]:
    """Expand results to include sibling chunks.

    Retrieves chunks immediately before and after each result
    to provide more context.

    Args:
        results: List of retrieved chunks
        table: LanceDB table for fetching siblings
        window: Number of siblings on each side (default: 1)

    Returns:
        Results with expanded context

    Note: This is a placeholder for future implementation.
    Requires additional indexing of chunk sequences.
    """
    # TODO: Implement sibling expansion when chunk sequence
    # indexing is added to the database schema
    return results


async def get_parent_content(
    parent_ids: list[str],
    table: Any,
) -> dict[str, str]:
    """Retrieve full content for parent documents.

    Args:
        parent_ids: List of parent IDs to retrieve
        table: LanceDB table

    Returns:
        Dictionary mapping parent_id to content

    Note: This is a placeholder for future implementation.
    Requires parent content storage in database.
    """
    # TODO: Implement when parent content storage is added
    return {}
