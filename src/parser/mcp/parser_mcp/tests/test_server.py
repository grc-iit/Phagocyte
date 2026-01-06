"""Unit tests for parser MCP server."""


from parser_mcp.server import (
    BatchInput,
    BatchResult,
    CitationPaper,
    CitationsInput,
    DoiBibInput,
    DoiBibResult,
    ParseRefsInput,
    ParseRefsResult,
    RetrieveInput,
    RetrieveResult,
    VerifyInput,
    VerifyResult,
)


class TestRetrieveInput:
    """Test RetrieveInput model."""

    def test_default_values(self) -> None:
        """Test default input values."""
        input = RetrieveInput(identifier="10.1234/test")

        assert input.identifier == "10.1234/test"
        assert input.output_dir == "./papers"
        assert input.skip_existing is True
        assert input.verbose is False

    def test_custom_values(self) -> None:
        """Test custom input values."""
        input = RetrieveInput(
            identifier="arXiv:2005.14165",
            output_dir="/custom/papers",
            email="test@example.com",
            skip_existing=False,
            verbose=True,
        )

        assert input.identifier == "arXiv:2005.14165"
        assert input.output_dir == "/custom/papers"
        assert input.email == "test@example.com"


class TestRetrieveResult:
    """Test RetrieveResult model."""

    def test_success_result(self) -> None:
        """Test successful retrieval result."""
        result = RetrieveResult(
            success=True,
            pdf_path="/path/to/paper.pdf",
            source="arxiv",
            title="Test Paper",
        )

        assert result.success is True
        assert result.pdf_path is not None
        assert result.source == "arxiv"

    def test_failed_result(self) -> None:
        """Test failed retrieval result."""
        result = RetrieveResult(
            success=False,
            error="Paper not found",
        )

        assert result.success is False
        assert result.error == "Paper not found"

    def test_skipped_result(self) -> None:
        """Test skipped result."""
        result = RetrieveResult(
            success=True,
            pdf_path="/path/to/paper.pdf",
            skipped=True,
        )

        assert result.skipped is True


class TestBatchInput:
    """Test BatchInput model."""

    def test_default_values(self) -> None:
        """Test default batch values."""
        input = BatchInput(input_file="papers.txt")

        assert input.input_file == "papers.txt"
        assert input.output_dir == "./papers"
        assert input.concurrent == 3

    def test_concurrent_limits(self) -> None:
        """Test concurrent download limits."""
        input = BatchInput(input_file="papers.txt", concurrent=10)
        assert input.concurrent == 10


class TestBatchResult:
    """Test BatchResult model."""

    def test_batch_stats(self) -> None:
        """Test batch result statistics."""
        result = BatchResult(
            total=10,
            succeeded=8,
            failed=1,
            skipped=1,
            results=[],
        )

        assert result.total == 10
        assert result.succeeded == 8
        assert result.failed == 1
        assert result.skipped == 1


class TestParseRefsInput:
    """Test ParseRefsInput model."""

    def test_default_values(self) -> None:
        """Test default parse values."""
        input = ParseRefsInput(input_file="research.md")

        assert input.input_file == "research.md"
        assert input.output_dir == "./parsed"
        assert input.agent == "none"
        assert input.export_batch is True
        assert input.export_dois is True

    def test_agent_options(self) -> None:
        """Test agent options."""
        for agent in ["none", "claude", "gemini"]:
            input = ParseRefsInput(input_file="test.md", agent=agent)
            assert input.agent == agent


class TestParseRefsResult:
    """Test ParseRefsResult model."""

    def test_success_result(self) -> None:
        """Test successful parse result."""
        result = ParseRefsResult(
            success=True,
            total_references=25,
            json_path="/path/refs.json",
            markdown_path="/path/refs.md",
            agent_used="claude",
        )

        assert result.success is True
        assert result.total_references == 25
        assert result.agent_used == "claude"


class TestDoiBibInput:
    """Test DoiBibInput model."""

    def test_dois_list(self) -> None:
        """Test DOIs list input."""
        input = DoiBibInput(dois=["10.1234/a", "10.1234/b"])

        assert len(input.dois) == 2

    def test_with_output(self) -> None:
        """Test with output file."""
        input = DoiBibInput(
            dois=["10.1234/test"],
            output_file="refs.bib",
        )

        assert input.output_file == "refs.bib"


class TestDoiBibResult:
    """Test DoiBibResult model."""

    def test_conversion_stats(self) -> None:
        """Test conversion statistics."""
        result = DoiBibResult(
            success=True,
            total=5,
            converted=4,
            failed=1,
            bibtex="@article{...}",
        )

        assert result.total == 5
        assert result.converted == 4


class TestVerifyInput:
    """Test VerifyInput model."""

    def test_default_values(self) -> None:
        """Test default verify values."""
        input = VerifyInput(input_path="refs.bib")

        assert input.input_path == "refs.bib"
        assert input.output_dir == "./verified"
        assert input.dry_run is False


class TestVerifyResult:
    """Test VerifyResult model."""

    def test_verification_stats(self) -> None:
        """Test verification statistics."""
        result = VerifyResult(
            success=True,
            verified=80,
            arxiv=10,
            searched=5,
            website=3,
            manual=2,
            total_verified=95,
        )

        assert result.total_verified == 95


class TestCitationsInput:
    """Test CitationsInput model."""

    def test_default_values(self) -> None:
        """Test default citations values."""
        input = CitationsInput(identifier="10.1234/test")

        assert input.identifier == "10.1234/test"
        assert input.direction == "both"
        assert input.limit == 50

    def test_direction_options(self) -> None:
        """Test direction options."""
        for direction in ["citations", "references", "both"]:
            input = CitationsInput(identifier="test", direction=direction)
            assert input.direction == direction


class TestCitationPaper:
    """Test CitationPaper model."""

    def test_paper_info(self) -> None:
        """Test citation paper information."""
        paper = CitationPaper(
            title="Test Paper",
            authors=["John Doe", "Jane Smith"],
            year=2023,
            doi="10.1234/test",
        )

        assert paper.title == "Test Paper"
        assert len(paper.authors) == 2
        assert paper.year == 2023


class TestMCPTools:
    """Test MCP tool registration."""

    def test_server_instantiation(self) -> None:
        """Test MCP server can be imported."""
        from parser_mcp.server import mcp

        assert mcp is not None
        assert mcp.name == "parser-mcp"

    def test_tools_registered(self) -> None:
        """Test key tools are registered."""
        from parser_mcp.server import (
            batch_retrieve,
            doi_to_bibtex,
            parse_references,
            retrieve_paper,
        )

        assert retrieve_paper is not None
        assert batch_retrieve is not None
        assert parse_references is not None
        assert doi_to_bibtex is not None
