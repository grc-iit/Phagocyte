"""Unit tests for processor MCP server."""


from processor_mcp.server import (
    DbStats,
    ExportResult,
    ProcessInput,
    ProcessResult,
    ServiceStatus,
    SetupResult,
)


class TestProcessInput:
    """Test ProcessInput model."""

    def test_default_values(self) -> None:
        """Test default input values."""
        input = ProcessInput(input_path="/path/to/docs")

        assert input.input_path == "/path/to/docs"
        assert input.output_db == "./lancedb"
        assert input.embedder == "ollama"
        assert input.text_profile == "low"
        assert input.code_profile == "low"
        assert input.table_mode == "separate"
        assert input.batch_size == 32
        assert input.incremental is True
        assert input.content_type == "auto"

    def test_custom_values(self) -> None:
        """Test custom input values."""
        input = ProcessInput(
            input_path="/docs",
            output_db="/custom/db",
            embedder="transformers",
            text_profile="high",
            code_profile="high",
            table_mode="unified",
            batch_size=64,
            incremental=False,
            content_type="code",
        )

        assert input.output_db == "/custom/db"
        assert input.embedder == "transformers"
        assert input.text_profile == "high"
        assert input.table_mode == "unified"
        assert input.content_type == "code"

    def test_embedder_options(self) -> None:
        """Test embedder options."""
        for embedder in ["ollama", "transformers"]:
            input = ProcessInput(input_path="/docs", embedder=embedder)
            assert input.embedder == embedder

    def test_profile_options(self) -> None:
        """Test profile options."""
        for text_profile in ["low", "medium", "high"]:
            input = ProcessInput(input_path="/docs", text_profile=text_profile)
            assert input.text_profile == text_profile

        for code_profile in ["low", "high"]:
            input = ProcessInput(input_path="/docs", code_profile=code_profile)
            assert input.code_profile == code_profile

    def test_table_mode_options(self) -> None:
        """Test table mode options."""
        for mode in ["separate", "unified", "both"]:
            input = ProcessInput(input_path="/docs", table_mode=mode)
            assert input.table_mode == mode

    def test_content_type_options(self) -> None:
        """Test content type options."""
        for ct in ["auto", "code", "paper", "markdown"]:
            input = ProcessInput(input_path="/docs", content_type=ct)
            assert input.content_type == ct


class TestProcessResult:
    """Test ProcessResult model."""

    def test_success_result(self) -> None:
        """Test successful processing result."""
        result = ProcessResult(
            files_processed=100,
            chunks_created=500,
            images_processed=25,
            errors=2,
            output_path="/output/lancedb",
        )

        assert result.files_processed == 100
        assert result.chunks_created == 500
        assert result.images_processed == 25
        assert result.errors == 2


class TestServiceStatus:
    """Test ServiceStatus model."""

    def test_all_services_available(self) -> None:
        """Test all services available."""
        status = ServiceStatus(
            ollama_cli=True,
            ollama_server=True,
            available_models=["nomic-embed-text", "mxbai-embed-large"],
            transformers_available=True,
            openclip_available=True,
        )

        assert status.ollama_cli is True
        assert status.ollama_server is True
        assert len(status.available_models) == 2
        assert status.transformers_available is True

    def test_no_services(self) -> None:
        """Test no services available."""
        status = ServiceStatus(
            ollama_cli=False,
            ollama_server=False,
            available_models=[],
            transformers_available=False,
            openclip_available=False,
        )

        assert status.ollama_cli is False
        assert len(status.available_models) == 0


class TestDbStats:
    """Test DbStats model."""

    def test_db_stats(self) -> None:
        """Test database statistics."""
        stats = DbStats(
            path="/path/to/lancedb",
            tables={
                "text_chunks": {"row_count": 1000},
                "code_chunks": {"row_count": 500},
            },
        )

        assert stats.path == "/path/to/lancedb"
        assert "text_chunks" in stats.tables


class TestExportResult:
    """Test ExportResult model."""

    def test_export_stats(self) -> None:
        """Test export statistics."""
        result = ExportResult(
            format="lance",
            tables={"text_chunks": 1000, "code_chunks": 500},
            total_rows=1500,
            output_path="/export/db",
        )

        assert result.format == "lance"
        assert result.total_rows == 1500


class TestSetupResult:
    """Test SetupResult model."""

    def test_setup_results(self) -> None:
        """Test model setup results."""
        result = SetupResult(
            results={
                "nomic-embed-text": {"status": "already_exists"},
                "mxbai-embed-large": {"status": "downloaded"},
            }
        )

        assert "nomic-embed-text" in result.results


class TestMCPTools:
    """Test MCP tool registration."""

    def test_server_instantiation(self) -> None:
        """Test MCP server can be imported."""
        from processor_mcp.server import mcp

        assert mcp is not None
        assert mcp.name == "processor-mcp"

    def test_tools_registered(self) -> None:
        """Test key tools are registered."""
        from processor_mcp.server import (
            check_services,
            get_db_stats,
            process_documents,
            setup_models,
        )

        assert process_documents is not None
        assert check_services is not None
        assert setup_models is not None
        assert get_db_stats is not None
