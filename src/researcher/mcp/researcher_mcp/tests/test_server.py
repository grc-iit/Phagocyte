"""Unit tests for researcher MCP server."""


from researcher_mcp.server import (
    ApiKeyStatus,
    ResearchInput,
    ResearchResult,
)


class TestResearchInput:
    """Test ResearchInput model."""

    def test_default_values(self) -> None:
        """Test default input values."""
        input = ResearchInput(query="Test query")

        assert input.query == "Test query"
        assert input.output_dir == "./output"
        assert input.mode == "undirected"
        assert input.artifacts == []
        assert input.max_wait == 3600
        assert input.verbose is False

    def test_custom_values(self) -> None:
        """Test custom input values."""
        input = ResearchInput(
            query="Deep learning",
            output_dir="/custom/output",
            mode="directed",
            artifacts=["https://example.com/paper.pdf"],
            max_wait=1800,
            verbose=True,
        )

        assert input.query == "Deep learning"
        assert input.output_dir == "/custom/output"
        assert input.mode == "directed"
        assert len(input.artifacts) == 1
        assert input.max_wait == 1800
        assert input.verbose is True

    def test_mode_validation(self) -> None:
        """Test mode enum validation."""
        # Valid modes
        for mode in ["undirected", "directed", "no-research"]:
            input = ResearchInput(query="test", mode=mode)
            assert input.mode == mode


class TestResearchResult:
    """Test ResearchResult model."""

    def test_success_result(self) -> None:
        """Test successful result."""
        result = ResearchResult(
            success=True,
            report_path="/path/to/report.md",
            metadata_path="/path/to/metadata.json",
            query="Test query",
            mode="undirected",
            duration_seconds=120.5,
        )

        assert result.success is True
        assert result.error is None
        assert result.duration_seconds == 120.5

    def test_failure_result(self) -> None:
        """Test failed result."""
        result = ResearchResult(
            success=False,
            query="Test query",
            mode="undirected",
            error="API key not found",
        )

        assert result.success is False
        assert result.error == "API key not found"
        assert result.report_path is None


class TestApiKeyStatus:
    """Test ApiKeyStatus model."""

    def test_key_status(self) -> None:
        """Test API key status model."""
        status = ApiKeyStatus(
            gemini_key_set=True,
            google_key_set=False,
            key_source="GEMINI_API_KEY",
        )

        assert status.gemini_key_set is True
        assert status.google_key_set is False
        assert status.key_source == "GEMINI_API_KEY"

    def test_no_keys(self) -> None:
        """Test when no keys are set."""
        status = ApiKeyStatus(
            gemini_key_set=False,
            google_key_set=False,
            key_source=None,
        )

        assert status.gemini_key_set is False
        assert status.google_key_set is False
        assert status.key_source is None


class TestMCPTools:
    """Test MCP tool registration."""

    def test_server_instantiation(self) -> None:
        """Test MCP server can be imported."""
        from researcher_mcp.server import mcp

        assert mcp is not None
        assert mcp.name == "researcher-mcp"

    def test_deep_research_tool_registered(self) -> None:
        """Test deep_research tool is registered."""
        from researcher_mcp.server import deep_research

        assert deep_research is not None
        assert callable(deep_research)
