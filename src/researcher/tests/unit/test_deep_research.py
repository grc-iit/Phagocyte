"""Unit tests for deep research module."""

from pathlib import Path

import pytest

from researcher.deep_research import (
    DeepResearcher,
    ResearchConfig,
    ResearchMode,
    ResearchStatus,
    _load_prompts_config,
    _post_process_report,
)


class TestResearchStatus:
    """Test ResearchStatus enum."""

    def test_status_values(self) -> None:
        """Test all status values are defined."""
        assert ResearchStatus.PENDING.value == "pending"
        assert ResearchStatus.IN_PROGRESS.value == "in_progress"
        assert ResearchStatus.COMPLETED.value == "completed"
        assert ResearchStatus.FAILED.value == "failed"
        assert ResearchStatus.CANCELLED.value == "cancelled"

    def test_status_count(self) -> None:
        """Test expected number of statuses."""
        assert len(ResearchStatus) == 5


class TestResearchMode:
    """Test ResearchMode enum."""

    def test_mode_values(self) -> None:
        """Test all mode values are defined."""
        assert ResearchMode.UNDIRECTED.value == "undirected"
        assert ResearchMode.DIRECTED.value == "directed"
        assert ResearchMode.NO_RESEARCH.value == "no_research"

    def test_mode_count(self) -> None:
        """Test expected number of modes."""
        assert len(ResearchMode) == 3


class TestResearchConfig:
    """Test ResearchConfig dataclass."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = ResearchConfig()

        assert config.output_format is None
        assert config.max_wait_time == 3600
        assert config.poll_interval == 10
        assert config.enable_streaming is True
        assert config.enable_thinking is True

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = ResearchConfig(
            output_format="Custom format",
            max_wait_time=7200,
            poll_interval=30,
            enable_streaming=False,
            enable_thinking=False,
        )

        assert config.output_format == "Custom format"
        assert config.max_wait_time == 7200
        assert config.poll_interval == 30
        assert config.enable_streaming is False
        assert config.enable_thinking is False


class TestPostProcessReport:
    """Test report post-processing."""

    def test_convert_single_citation(self) -> None:
        """Test converting [cite: N] to [N]."""
        input_text = "This is a claim [cite: 1] with citation."
        expected = "This is a claim [1] with citation."
        assert _post_process_report(input_text) == expected

    def test_convert_multiple_citations(self) -> None:
        """Test converting multiple citations."""
        input_text = "Studies show [cite: 1, 2, 3] various results."
        expected = "Studies show [1, 2, 3] various results."
        assert _post_process_report(input_text) == expected

    def test_convert_citation_with_spaces(self) -> None:
        """Test converting citations with various spacing."""
        input_text = "Evidence [cite:1] and [cite: 2] and [cite:  3]."
        expected = "Evidence [1] and [2] and [3]."
        assert _post_process_report(input_text) == expected

    def test_cleanup_multiple_blank_lines(self) -> None:
        """Test cleaning up excessive blank lines."""
        input_text = "Line 1\n\n\n\n\nLine 2"
        expected = "Line 1\n\nLine 2"
        assert _post_process_report(input_text) == expected

    def test_empty_input(self) -> None:
        """Test handling empty input."""
        assert _post_process_report("") == ""

    def test_none_input(self) -> None:
        """Test handling None input."""
        assert _post_process_report(None) is None

    def test_no_citations(self) -> None:
        """Test text without citations."""
        input_text = "Plain text without any citations."
        assert _post_process_report(input_text) == input_text


class TestLoadPromptsConfig:
    """Test prompts configuration loading."""

    def test_load_default_config(self, configs_dir: Path) -> None:
        """Test loading default prompts config."""
        config = _load_prompts_config()
        # Should return dict (possibly empty if file not found)
        assert isinstance(config, dict)

    def test_load_with_custom_path(self, tmp_path: Path) -> None:
        """Test loading config from custom path."""
        config_file = tmp_path / "prompts.yaml"
        config_file.write_text("default_output_format: Custom format")

        config = _load_prompts_config(config_file)
        assert config.get("default_output_format") == "Custom format"

    def test_custom_path_takes_precedence(self, tmp_path: Path) -> None:
        """Test that custom path takes precedence over defaults."""
        config_file = tmp_path / "custom_prompts.yaml"
        config_file.write_text("custom_key: custom_value")

        config = _load_prompts_config(config_file)
        assert config.get("custom_key") == "custom_value"


class TestDeepResearcher:
    """Test DeepResearcher class."""

    def test_instantiation_without_api_key(self, no_api_key: None) -> None:
        """Test that researcher can be instantiated without API key."""
        # Should not raise during instantiation
        researcher = DeepResearcher()
        assert researcher is not None

    def test_instantiation_with_api_key(self, mock_api_key: str) -> None:
        """Test researcher instantiation with API key."""
        researcher = DeepResearcher()
        assert researcher is not None

    def test_instantiation_with_explicit_key(self) -> None:
        """Test researcher with explicitly provided API key."""
        researcher = DeepResearcher(api_key="explicit-test-key")
        assert researcher is not None

    def test_config_defaults(self, mock_api_key: str) -> None:
        """Test researcher uses default config."""
        researcher = DeepResearcher()
        # Default config should be applied
        assert researcher.config is not None
        assert researcher.config.max_wait_time == 3600


class TestResearchModes:
    """Test different research modes."""

    @pytest.fixture
    def researcher(self, mock_api_key: str) -> DeepResearcher:
        """Create researcher instance."""
        return DeepResearcher()

    def test_undirected_mode_config(self) -> None:
        """Test undirected mode configuration."""
        config = ResearchConfig(mode=ResearchMode.UNDIRECTED)
        assert config.mode == ResearchMode.UNDIRECTED

    def test_directed_mode_config(self) -> None:
        """Test directed mode configuration."""
        config = ResearchConfig(
            mode=ResearchMode.DIRECTED,
            artifacts=["https://example.com/paper.pdf"],
        )
        assert config.mode == ResearchMode.DIRECTED
        assert len(config.artifacts) == 1

    def test_no_research_mode_config(self) -> None:
        """Test no-research mode configuration."""
        config = ResearchConfig(
            mode=ResearchMode.NO_RESEARCH,
            artifacts=["Local analysis content"],
        )
        assert config.mode == ResearchMode.NO_RESEARCH
