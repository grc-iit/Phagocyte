"""Pytest configuration and shared fixtures for parser tests."""

from pathlib import Path

import pytest

# ============================================================================
# Path Fixtures
# ============================================================================

@pytest.fixture
def fixtures_dir() -> Path:
    """Path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def papers_dir() -> Path:
    """Path to papers directory."""
    return Path(__file__).parent.parent / "papers"


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Temporary output directory for tests."""
    out = tmp_path / "output"
    out.mkdir()
    return out


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_research_text() -> str:
    """Sample research text with references."""
    return """# Research Report on Machine Learning

## Introduction

Recent advances in deep learning have transformed AI [[1]](#ref-1).
The transformer architecture [[2]](#ref-2) has enabled breakthroughs.

## Key Papers

- Attention Is All You Need (Vaswani et al., 2017)
- BERT (Devlin et al., 2019) - arXiv:1810.04805
- GPT-3 (Brown et al., 2020) - https://arxiv.org/abs/2005.14165

## Code Resources

- GitHub: huggingface/transformers
- GitHub: https://github.com/openai/gpt-3

## References

1. Goodfellow, I. et al. "Deep Learning." MIT Press, 2016.
2. Vaswani, A. et al. "Attention Is All You Need." NeurIPS 2017. DOI: 10.5555/3295222.3295349
"""


@pytest.fixture
def sample_github_text() -> str:
    """Sample text with GitHub references."""
    return """
Check out these repositories:
- `huggingface/transformers` - Main library
- github.com/pytorch/pytorch
- **Repository:** `openai/whisper`
"""


@pytest.fixture
def sample_arxiv_text() -> str:
    """Sample text with arXiv references."""
    return """
Key papers:
- arXiv:2005.14165 (GPT-3)
- https://arxiv.org/abs/1810.04805 (BERT)
- arxiv.org/pdf/2301.12345
"""


@pytest.fixture
def sample_doi_text() -> str:
    """Sample text with DOI references."""
    return """
Citations with DOIs:
- DOI: 10.1038/nature14539
- https://doi.org/10.1145/3442188.3445922
- doi.org/10.5555/3295222.3295349
"""


@pytest.fixture
def sample_youtube_text() -> str:
    """Sample text with YouTube references."""
    return """
Video resources:
- https://www.youtube.com/watch?v=dQw4w9WgXcQ
- https://youtu.be/abc123xyz
"""


@pytest.fixture
def sample_bibtex() -> str:
    """Sample BibTeX content."""
    return """@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and others},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}

@inproceedings{devlin2019bert,
  title={BERT: Pre-training of Deep Bidirectional Transformers},
  author={Devlin, Jacob and others},
  booktitle={NAACL},
  year={2019}
}
"""


# ============================================================================
# Identifier Fixtures
# ============================================================================

@pytest.fixture
def valid_doi() -> str:
    """A valid DOI string."""
    return "10.1038/nature14539"


@pytest.fixture
def valid_arxiv_id() -> str:
    """A valid arXiv ID."""
    return "2005.14165"


@pytest.fixture
def valid_pmid() -> str:
    """A valid PubMed ID."""
    return "33929527"


# ============================================================================
# Markers Configuration
# ============================================================================

def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--live-api",
        action="store_true",
        help="Run tests against live APIs (CrossRef, arXiv, etc.)",
    )
    parser.addoption(
        "--slow",
        action="store_true",
        help="Run slow tests (e.g., paper downloads)",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Skip live API and slow tests unless flags are set."""
    if not config.getoption("--live-api"):
        skip_live = pytest.mark.skip(reason="need --live-api option to run")
        for item in items:
            if "live_api" in item.keywords:
                item.add_marker(skip_live)

    if not config.getoption("--slow"):
        skip_slow = pytest.mark.skip(reason="need --slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
