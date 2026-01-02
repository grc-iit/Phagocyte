"""Pytest configuration and shared fixtures for root CLI tests."""

import pytest
from pathlib import Path
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def sample_markdown_file(tmp_workspace: Path) -> Path:
    """Create a sample markdown file."""
    md_file = tmp_workspace / "sample.md"
    md_file.write_text("""# Sample Research

## Introduction

This paper discusses machine learning [[1]](#ref-1).

## References

1. Author et al., "Paper Title", 2023.
""")
    return md_file


@pytest.fixture
def sample_code_file(tmp_workspace: Path) -> Path:
    """Create a sample Python file."""
    py_file = tmp_workspace / "sample.py"
    py_file.write_text('''"""Sample Python module."""

def hello_world():
    """Print hello world."""
    print("Hello, World!")

class Calculator:
    """Simple calculator."""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
''')
    return py_file


# ============================================================================
# Markers Configuration
# ============================================================================


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        help="Run integration tests that require module installations",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Skip integration tests unless flag is set."""
    if not config.getoption("--integration"):
        skip_integration = pytest.mark.skip(reason="need --integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
