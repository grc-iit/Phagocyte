"""Pytest configuration and shared fixtures."""

from pathlib import Path
from typing import Any

import pytest

from processor.config import ProcessorConfig
from processor.types import Chunk, ContentType, ImageChunk


@pytest.fixture
def fixtures_dir() -> Path:
    """Path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def input_dir() -> Path:
    """Path to input data directory."""
    return Path(__file__).parent.parent.parent / "input"


@pytest.fixture
def input_reduced_dir() -> Path:
    """Path to input_reduced test data directory.

    Checks tests/fixtures/input_reduced first, falls back to project root.
    """
    fixtures_path = Path(__file__).parent / "fixtures" / "input_reduced"
    if fixtures_path.exists():
        return fixtures_path
    # Fall back to project root
    return Path(__file__).parent.parent / "input_reduced"


@pytest.fixture
def sample_python_code() -> str:
    """Sample Python code for testing."""
    return '''
def hello_world():
    """Print hello world."""
    print("Hello, World!")

class Calculator:
    """Simple calculator class."""

    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract two numbers."""
        return a - b
'''


@pytest.fixture
def sample_cpp_code() -> str:
    """Sample C++ code for testing."""
    return '''
#include <iostream>
#include <string>

namespace example {

class Greeter {
public:
    void greet(const std::string& name) {
        std::cout << "Hello, " << name << "!" << std::endl;
    }
};

int main() {
    Greeter g;
    g.greet("World");
    return 0;
}

}  // namespace example
'''


@pytest.fixture
def sample_markdown() -> str:
    """Sample markdown for testing."""
    return '''
# Introduction

This is the introduction section.

## Background

Some background information here.

### Technical Details

More detailed technical information.

## Methodology

Description of the methodology.

## Results

The results of the study.

## Conclusion

Final conclusions.
'''


@pytest.fixture
def sample_paper_markdown() -> str:
    """Sample academic paper markdown."""
    return '''
# Paper Title

## Abstract

This paper presents a novel approach to solving problem X [[1]](#ref-1) [[2]](#ref-2).

## I. Introduction

Traditional approaches have limitations [[3]](#ref-3). We propose a new method.

## II. Background

Previous work includes [[4]](#ref-4) and [[5]](#ref-5).

## III. Methodology

Our approach consists of three steps.

## IV. Results

We achieved 95% accuracy.

## V. Conclusion

The proposed method outperforms baselines.

## References

1. Author et al., "Paper 1", 2020
2. Author et al., "Paper 2", 2021
'''


@pytest.fixture
def temp_lancedb(tmp_path: Path) -> Path:
    """Temporary LanceDB directory."""
    db_path = tmp_path / "lancedb"
    db_path.mkdir()
    return db_path


@pytest.fixture
def config(temp_lancedb: Path) -> ProcessorConfig:
    """Default test configuration."""
    return ProcessorConfig(
        database={"uri": str(temp_lancedb)},
        processing={"incremental": False},
    )


@pytest.fixture
def mock_embedding() -> list[float]:
    """Mock embedding vector (768d zeros)."""
    return [0.0] * 768


@pytest.fixture
def sample_chunk(mock_embedding: list[float]) -> Chunk:
    """Sample chunk for testing."""
    chunk = Chunk.create(
        content="Sample chunk content for testing",
        source_file="/test/file.py",
        source_type=ContentType.CODE_PYTHON,
        language="python",
    )
    chunk.embedding = mock_embedding
    return chunk


# Markers for network/slow tests
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--ollama", action="store_true", help="Run Ollama tests")


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if not config.getoption("--ollama"):
        skip_ollama = pytest.mark.skip(reason="need --ollama option")
        for item in items:
            if "ollama" in item.keywords:
                item.add_marker(skip_ollama)


@pytest.fixture
def sample_figure_data() -> dict[str, Any]:
    """Sample figure data from figures.json."""
    return {
        "figure_id": 1,
        "caption": "Figure 1: System architecture",
        "classification": "flowchart (0.95)",
        "description": "A flowchart showing the system architecture.",
        "page": 3,
        "image_path": "./img/figure1.png",
    }


@pytest.fixture
def sample_image_chunk(tmp_path: Path, sample_figure_data: dict[str, Any]) -> ImageChunk:
    """Sample ImageChunk for testing."""
    # Create directory structure
    paper_dir = tmp_path / "test-paper"
    paper_dir.mkdir()
    img_dir = paper_dir / "img"
    img_dir.mkdir()
    (img_dir / "figure1.png").write_bytes(b"fake image data")

    chunk = ImageChunk.from_figure_json(sample_figure_data, paper_dir)
    chunk.text_embedding = [0.0] * 1024
    chunk.visual_embedding = [0.0] * 1024
    return chunk


@pytest.fixture
def mock_text_embedding() -> list[float]:
    """Mock text embedding vector (1024d zeros for stella)."""
    return [0.0] * 1024


@pytest.fixture
def mock_visual_embedding() -> list[float]:
    """Mock visual embedding vector (1024d zeros for CLIP)."""
    return [0.0] * 1024
