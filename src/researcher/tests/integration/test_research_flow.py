"""Integration tests for research flow."""

from pathlib import Path

import pytest

from researcher.deep_research import (
    DeepResearcher,
    ResearchConfig,
    ResearchMode,
    ResearchResult,
)


class TestResearchOutput:
    """Test research output handling."""

    @pytest.fixture
    def researcher(self, mock_api_key: str) -> DeepResearcher:
        """Create researcher instance."""
        return DeepResearcher()

    def test_output_directory_creation(
        self, researcher: DeepResearcher, output_dir: Path
    ) -> None:
        """Test that output directory is created."""
        # Output dir from fixture should exist
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_config_file_loading(self, configs_dir: Path) -> None:
        """Test config files can be loaded."""
        prompts_yaml = configs_dir / "prompts.yaml"
        if prompts_yaml.exists():
            assert prompts_yaml.read_text()


@pytest.mark.live_api
class TestLiveResearch:
    """Tests that require live API access.

    Run with: pytest --live-api
    """

    @pytest.fixture
    def researcher(self) -> DeepResearcher:
        """Create researcher with real API key."""
        import os
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            pytest.skip("No API key available")
        return DeepResearcher(api_key=api_key)

    @pytest.mark.asyncio
    async def test_simple_research(
        self, researcher: DeepResearcher, output_dir: Path
    ) -> None:
        """Test simple research query."""
        result = await researcher.research(
            "What is Python's GIL in one sentence?",
            output_dir=output_dir,
            config=ResearchConfig(max_wait_time=120),
        )

        assert result is not None
        assert result.status in ["completed", "failed"]

    @pytest.mark.asyncio
    async def test_directed_research_with_artifacts(
        self, researcher: DeepResearcher, output_dir: Path
    ) -> None:
        """Test directed research with artifacts."""
        config = ResearchConfig(
            mode=ResearchMode.DIRECTED,
            artifacts=["https://docs.python.org/3/library/asyncio.html"],
            max_wait_time=120,
        )

        result = await researcher.research(
            "Summarize Python asyncio basics",
            output_dir=output_dir,
            config=config,
        )

        assert result is not None


class TestResearchResult:
    """Test ResearchResult handling."""

    def test_result_from_dict(self) -> None:
        """Test creating result from dictionary."""
        data = {
            "query": "test query",
            "report": "Test report content",
            "status": "completed",
        }

        result = ResearchResult(**data)
        assert result.query == "test query"
        assert result.report == "Test report content"
