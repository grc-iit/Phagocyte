"""API clients for paper acquisition.

Provides clients for:
- Semantic Scholar: Paper search and metadata
- CrossRef: DOI resolution and metadata
- OpenAlex: Academic metadata and citations
- Unpaywall: Open access PDF locations
- arXiv: Preprint access and download
- PMC: PubMed Central biomedical literature
- bioRxiv/medRxiv: Biology and medical preprints (with Selenium fallback)
- ACL Anthology: NLP conference papers (ACL, EMNLP, NAACL, etc.)
- Frontiers: Gold OA papers (with Selenium for bot protection)
- Institutional: EZProxy and VPN access
- WebSearch: Claude Agent SDK web search for legal PDFs
- Sci-Hub: Unofficial PDF access (⚠️ legal concerns)
- LibGen: Unofficial PDF access (⚠️ legal concerns)
"""

from .acl_anthology import ACLAnthologyClient
from .arxiv import ArxivClient
from .base import BaseClient, RateLimiter
from .biorxiv import BioRxivClient
from .crossref import CrossRefClient
from .frontiers import FrontiersClient
from .institutional import InstitutionalAccessClient
from .libgen import LibGenClient
from .openalex import OpenAlexClient
from .pmc import PMCClient
from .scihub import ScihubClient
from .semantic_scholar import SemanticScholarClient
from .unpaywall import UnpaywallClient
from .web_search import WebSearchClient

__all__ = [
    "BaseClient",
    "RateLimiter",
    "SemanticScholarClient",
    "CrossRefClient",
    "OpenAlexClient",
    "UnpaywallClient",
    "ArxivClient",
    "PMCClient",
    "BioRxivClient",
    "ACLAnthologyClient",
    "FrontiersClient",
    "InstitutionalAccessClient",
    "WebSearchClient",
    "ScihubClient",
    "LibGenClient",
]
