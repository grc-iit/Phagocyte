# Parser Acquisition Module

> Paper retrieval with multi-source fallback

This module handles downloading scientific papers from multiple sources.

**See the main [README.md](../../../README.md) for full documentation.**

## Quick Reference

### CLI Commands

```bash
# Single paper (DOI preferred for peer-reviewed papers)
parser retrieve --doi "10.1038/nature12373"
parser retrieve --title "Attention Is All You Need"
parser retrieve arXiv:1706.03762

# Batch download
parser batch papers.csv -o ./output

# Check sources
parser sources

# Configure institutional access
parser auth --proxy-url "https://ezproxy.university.edu/login?url="
```

### Python API

```python
from parser.acquisition import PaperRetriever, Config

config = Config.load()
retriever = PaperRetriever(config)

result = await retriever.retrieve(doi="10.1038/nature12373", output_dir="./papers")
```

## Retrieval Strategy

### Metadata Resolution Order (Peer-Reviewed First)

| Priority | Source | Type | Purpose |
|----------|--------|------|---------|
| 1 | CrossRef | Peer-reviewed | Most authoritative for published papers |
| 2 | Semantic Scholar | Both | Good coverage, DOI/arXiv support |
| 3 | OpenAlex | Both | Broad coverage fallback |
| 4 | arXiv | Preprints | Fallback when peer-reviewed not found |

### Per-Source Download Order

**arXiv:** arXiv ID → arXiv URL → Title search (70% threshold)

**Sci-Hub/LibGen:** Title first → DOI fallback (configurable via `lookup_priority`)

### DOI Validation

Automatically skips problematic DOIs:
- **Peer reviews** (`10.14293/...sor-...`) - Not the actual paper
- **Book chapters** (`10.1007/978-`, `10.1016/b978-`, `10.1201/978...`) - Often paywalled reprints
- **Datasets** (`10.5281/zenodo...`) - Not papers

### Title Mismatch Detection

Catches false positives for confusing terms (llama vs LLaMA, falcon vs Falcon LLM, etc.)

## Module Structure

```
acquisition/
├── __init__.py         # Public exports
├── config.py           # Configuration handling
├── retriever.py        # Main PaperRetriever class
├── identifier.py       # DOI/arXiv ID resolution
└── clients/            # API clients
    ├── base.py         # BaseClient with rate limiting
    ├── arxiv.py        # arXiv API
    ├── crossref.py     # CrossRef API
    ├── unpaywall.py    # Unpaywall API
    ├── semantic_scholar.py
    ├── openalex.py
    ├── pmc.py          # PubMed Central
    ├── biorxiv.py      # bioRxiv/medRxiv
    ├── institutional.py # EZProxy/VPN support
    ├── scihub.py       # Sci-Hub (disabled by default)
    ├── libgen.py       # LibGen (disabled by default)
    └── web_search.py   # Google Scholar fallback
```

## Configuration

See [config.yaml](../../../config.yaml) for full configuration options.

Key settings:
- `sources.<name>.enabled` - Enable/disable each source
- `sources.<name>.priority` - Source priority (lower = tried first)
- `download.lookup_priority` - Title vs DOI search order
- `download.skip_existing` - Skip already downloaded papers
