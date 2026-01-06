"""Pytest configuration and shared fixtures for researcher tests."""

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
def configs_dir() -> Path:
    """Path to configs directory."""
    return Path(__file__).parent.parent / "configs"


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
def sample_research_query() -> str:
    """Sample research query for testing."""
    return "What are the best practices for HDF5 file optimization?"


@pytest.fixture
def sample_research_report() -> str:
    """Sample research report output."""
    return """# Research Report: HDF5 Best Practices

## Abstract

This report examines HDF5 file optimization strategies.

## 1. Introduction

HDF5 (Hierarchical Data Format 5) is widely used for scientific data [[1]](#ref-1).

## 2. Methodology

We analyzed various optimization techniques.

## 3. Results

Key findings include chunking strategies and compression [[2]](#ref-2).

## 4. Conclusion

Proper configuration significantly improves performance.

## References

1. The HDF Group. "HDF5 Documentation." https://www.hdfgroup.org/
2. Folk, M. et al. "An overview of the HDF5 technology suite." 2011.
"""


@pytest.fixture
def sample_artifacts() -> list[str]:
    """Sample artifacts for directed research."""
    return [
        "https://www.hdfgroup.org/solutions/hdf5/",
        "https://docs.h5py.org/en/stable/",
    ]


# ============================================================================
# Environment Fixtures
# ============================================================================

@pytest.fixture
def mock_api_key(monkeypatch: pytest.MonkeyPatch) -> str:
    """Mock API key for testing."""
    key = "test-api-key-12345"
    monkeypatch.setenv("GEMINI_API_KEY", key)
    return key


@pytest.fixture
def no_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove API key from environment."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)


# ============================================================================
# Markers Configuration
# ============================================================================

def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--live-api",
        action="store_true",
        help="Run tests against live Gemini API (requires API key)",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Skip live API tests unless --live-api flag is set."""
    if not config.getoption("--live-api"):
        skip_live = pytest.mark.skip(reason="need --live-api option to run")
        for item in items:
            if "live_api" in item.keywords:
                item.add_marker(skip_live)
