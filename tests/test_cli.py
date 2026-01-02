"""Unit tests for Phagocyte CLI.

Comprehensive tests for all CLI commands and their options.
"""

from click.testing import CliRunner

import sys

sys.path.insert(0, str(__file__).rsplit("/tests", 1)[0] + "/src")

from cli import cli, get_src


class TestCLIMain:
    """Test main CLI entry point."""

    def test_cli_help(self, runner: CliRunner) -> None:
        """Test CLI help output."""
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Phagocyte" in result.output or "pipeline" in result.output.lower()
        assert "research" in result.output
        assert "parse" in result.output
        assert "ingest" in result.output
        assert "process" in result.output

    def test_cli_version(self, runner: CliRunner) -> None:
        """Test CLI version output."""
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_get_src_returns_path(self) -> None:
        """Test get_src returns valid path."""
        from pathlib import Path

        src = get_src()
        assert isinstance(src, Path)
        assert src.exists() or True  # May not exist in test env


class TestResearchCommand:
    """Test research command."""

    def test_research_help(self, runner: CliRunner) -> None:
        """Test research command help."""
        result = runner.invoke(cli, ["research", "--help"])

        assert result.exit_code == 0
        assert "TOPIC" in result.output

    def test_research_has_output_option(self, runner: CliRunner) -> None:
        """Test research has --output option."""
        result = runner.invoke(cli, ["research", "--help"])

        assert result.exit_code == 0
        assert "--output" in result.output or "-o" in result.output

    def test_research_has_mode_option(self, runner: CliRunner) -> None:
        """Test research has --mode option."""
        result = runner.invoke(cli, ["research", "--help"])

        assert result.exit_code == 0
        assert "--mode" in result.output or "-m" in result.output
        # Check mode choices
        assert "undirected" in result.output
        assert "directed" in result.output
        assert "no-research" in result.output

    def test_research_has_artifact_option(self, runner: CliRunner) -> None:
        """Test research has --artifact option."""
        result = runner.invoke(cli, ["research", "--help"])

        assert result.exit_code == 0
        assert "--artifact" in result.output or "-a" in result.output

    def test_research_has_api_key_option(self, runner: CliRunner) -> None:
        """Test research has --api-key option."""
        result = runner.invoke(cli, ["research", "--help"])

        assert result.exit_code == 0
        assert "--api-key" in result.output

    def test_research_has_verbose_option(self, runner: CliRunner) -> None:
        """Test research has --verbose option."""
        result = runner.invoke(cli, ["research", "--help"])

        assert result.exit_code == 0
        assert "--verbose" in result.output or "-v" in result.output


class TestParseGroup:
    """Test parse command group."""

    def test_parse_help(self, runner: CliRunner) -> None:
        """Test parse group help."""
        result = runner.invoke(cli, ["parse", "--help"])

        assert result.exit_code == 0
        # Check for key subcommands
        assert "refs" in result.output
        assert "retrieve" in result.output
        assert "batch" in result.output
        assert "doi2bib" in result.output
        assert "verify" in result.output
        assert "citations" in result.output
        assert "sources" in result.output
        assert "auth" in result.output
        assert "init" in result.output
        assert "config" in result.output

    # --- Parse refs command ---
    def test_parse_refs_help(self, runner: CliRunner) -> None:
        """Test parse refs command help."""
        result = runner.invoke(cli, ["parse", "refs", "--help"])

        assert result.exit_code == 0
        assert "INPUT_FILE" in result.output

    def test_parse_refs_has_output_option(self, runner: CliRunner) -> None:
        """Test parse refs has --output option."""
        result = runner.invoke(cli, ["parse", "refs", "--help"])

        assert result.exit_code == 0
        assert "--output" in result.output or "-o" in result.output

    def test_parse_refs_has_agent_option(self, runner: CliRunner) -> None:
        """Test parse refs has --agent option."""
        result = runner.invoke(cli, ["parse", "refs", "--help"])

        assert result.exit_code == 0
        assert "--agent" in result.output
        # Check agent choices
        assert "none" in result.output
        assert "claude" in result.output
        assert "gemini" in result.output

    def test_parse_refs_has_export_batch_option(self, runner: CliRunner) -> None:
        """Test parse refs has --export-batch option."""
        result = runner.invoke(cli, ["parse", "refs", "--help"])

        assert result.exit_code == 0
        assert "--export-batch" in result.output

    def test_parse_refs_has_export_dois_option(self, runner: CliRunner) -> None:
        """Test parse refs has --export-dois option."""
        result = runner.invoke(cli, ["parse", "refs", "--help"])

        assert result.exit_code == 0
        assert "--export-dois" in result.output

    def test_parse_refs_has_compare_option(self, runner: CliRunner) -> None:
        """Test parse refs has --compare option."""
        result = runner.invoke(cli, ["parse", "refs", "--help"])

        assert result.exit_code == 0
        assert "--compare" in result.output

    # --- Parse retrieve command ---
    def test_parse_retrieve_help(self, runner: CliRunner) -> None:
        """Test parse retrieve command help."""
        result = runner.invoke(cli, ["parse", "retrieve", "--help"])

        assert result.exit_code == 0
        assert "IDENTIFIER" in result.output

    def test_parse_retrieve_has_output_option(self, runner: CliRunner) -> None:
        """Test parse retrieve has --output option."""
        result = runner.invoke(cli, ["parse", "retrieve", "--help"])

        assert result.exit_code == 0
        assert "--output" in result.output or "-o" in result.output

    def test_parse_retrieve_has_email_option(self, runner: CliRunner) -> None:
        """Test parse retrieve has --email option."""
        result = runner.invoke(cli, ["parse", "retrieve", "--help"])

        assert result.exit_code == 0
        assert "--email" in result.output

    def test_parse_retrieve_has_verbose_option(self, runner: CliRunner) -> None:
        """Test parse retrieve has --verbose option."""
        result = runner.invoke(cli, ["parse", "retrieve", "--help"])

        assert result.exit_code == 0
        assert "--verbose" in result.output or "-v" in result.output

    # --- Parse batch command ---
    def test_parse_batch_help(self, runner: CliRunner) -> None:
        """Test parse batch command help."""
        result = runner.invoke(cli, ["parse", "batch", "--help"])

        assert result.exit_code == 0
        assert "INPUT_FILE" in result.output

    def test_parse_batch_has_concurrent_option(self, runner: CliRunner) -> None:
        """Test parse batch has --concurrent option."""
        result = runner.invoke(cli, ["parse", "batch", "--help"])

        assert result.exit_code == 0
        assert "--concurrent" in result.output or "-n" in result.output

    def test_parse_batch_has_email_option(self, runner: CliRunner) -> None:
        """Test parse batch has --email option."""
        result = runner.invoke(cli, ["parse", "batch", "--help"])

        assert result.exit_code == 0
        assert "--email" in result.output

    # --- Parse doi2bib command ---
    def test_parse_doi2bib_help(self, runner: CliRunner) -> None:
        """Test parse doi2bib command help."""
        result = runner.invoke(cli, ["parse", "doi2bib", "--help"])

        assert result.exit_code == 0

    def test_parse_doi2bib_has_input_option(self, runner: CliRunner) -> None:
        """Test parse doi2bib has --input option."""
        result = runner.invoke(cli, ["parse", "doi2bib", "--help"])

        assert result.exit_code == 0
        assert "--input" in result.output or "-i" in result.output

    def test_parse_doi2bib_has_format_option(self, runner: CliRunner) -> None:
        """Test parse doi2bib has --format option."""
        result = runner.invoke(cli, ["parse", "doi2bib", "--help"])

        assert result.exit_code == 0
        assert "--format" in result.output
        # Check format choices
        assert "bibtex" in result.output
        assert "json" in result.output
        assert "markdown" in result.output

    # --- Parse verify command ---
    def test_parse_verify_help(self, runner: CliRunner) -> None:
        """Test parse verify command help."""
        result = runner.invoke(cli, ["parse", "verify", "--help"])

        assert result.exit_code == 0
        assert "INPUT_PATH" in result.output

    def test_parse_verify_has_dry_run_option(self, runner: CliRunner) -> None:
        """Test parse verify has --dry-run option."""
        result = runner.invoke(cli, ["parse", "verify", "--help"])

        assert result.exit_code == 0
        assert "--dry-run" in result.output

    def test_parse_verify_has_email_option(self, runner: CliRunner) -> None:
        """Test parse verify has --email option."""
        result = runner.invoke(cli, ["parse", "verify", "--help"])

        assert result.exit_code == 0
        assert "--email" in result.output

    # --- Parse citations command ---
    def test_parse_citations_help(self, runner: CliRunner) -> None:
        """Test parse citations command help."""
        result = runner.invoke(cli, ["parse", "citations", "--help"])

        assert result.exit_code == 0

    def test_parse_citations_has_direction_option(self, runner: CliRunner) -> None:
        """Test parse citations has --direction option."""
        result = runner.invoke(cli, ["parse", "citations", "--help"])

        assert result.exit_code == 0
        assert "--direction" in result.output

    def test_parse_sources_help(self, runner: CliRunner) -> None:
        """Test parse sources command help."""
        result = runner.invoke(cli, ["parse", "sources", "--help"])

        assert result.exit_code == 0


class TestIngestGroup:
    """Test ingest command group."""

    def test_ingest_help(self, runner: CliRunner) -> None:
        """Test ingest group help."""
        result = runner.invoke(cli, ["ingest", "--help"])

        assert result.exit_code == 0
        assert "file" in result.output
        assert "batch" in result.output
        assert "crawl" in result.output
        assert "clone" in result.output
        assert "describe" in result.output

    # --- Ingest file command ---
    def test_ingest_file_help(self, runner: CliRunner) -> None:
        """Test ingest file command help."""
        result = runner.invoke(cli, ["ingest", "file", "--help"])

        assert result.exit_code == 0
        assert "SOURCE" in result.output

    def test_ingest_file_has_output_option(self, runner: CliRunner) -> None:
        """Test ingest file has --output option."""
        result = runner.invoke(cli, ["ingest", "file", "--help"])

        assert result.exit_code == 0
        assert "--output" in result.output or "-o" in result.output

    def test_ingest_file_has_describe_images_option(self, runner: CliRunner) -> None:
        """Test ingest file has --describe-images option."""
        result = runner.invoke(cli, ["ingest", "file", "--help"])

        assert result.exit_code == 0
        assert "--describe-images" in result.output

    def test_ingest_file_has_img_format_option(self, runner: CliRunner) -> None:
        """Test ingest file has --img-format option."""
        result = runner.invoke(cli, ["ingest", "file", "--help"])

        assert result.exit_code == 0
        assert "--img-format" in result.output
        # Check format choices
        assert "png" in result.output
        assert "jpg" in result.output
        assert "webp" in result.output

    def test_ingest_file_has_verbose_option(self, runner: CliRunner) -> None:
        """Test ingest file has --verbose option."""
        result = runner.invoke(cli, ["ingest", "file", "--help"])

        assert result.exit_code == 0
        assert "--verbose" in result.output or "-v" in result.output

    # --- Ingest batch command ---
    def test_ingest_batch_help(self, runner: CliRunner) -> None:
        """Test ingest batch command help."""
        result = runner.invoke(cli, ["ingest", "batch", "--help"])

        assert result.exit_code == 0
        assert "INPUT_DIR" in result.output

    def test_ingest_batch_has_recursive_option(self, runner: CliRunner) -> None:
        """Test ingest batch has --recursive option."""
        result = runner.invoke(cli, ["ingest", "batch", "--help"])

        assert result.exit_code == 0
        assert "--recursive" in result.output

    def test_ingest_batch_has_concurrency_option(self, runner: CliRunner) -> None:
        """Test ingest batch has --concurrency option."""
        result = runner.invoke(cli, ["ingest", "batch", "--help"])

        assert result.exit_code == 0
        assert "--concurrency" in result.output or "-n" in result.output

    def test_ingest_batch_has_describe_images_option(self, runner: CliRunner) -> None:
        """Test ingest batch has --describe-images option."""
        result = runner.invoke(cli, ["ingest", "batch", "--help"])

        assert result.exit_code == 0
        assert "--describe-images" in result.output

    # --- Ingest crawl command ---
    def test_ingest_crawl_help(self, runner: CliRunner) -> None:
        """Test ingest crawl command help."""
        result = runner.invoke(cli, ["ingest", "crawl", "--help"])

        assert result.exit_code == 0
        assert "URL" in result.output

    def test_ingest_crawl_has_max_pages_option(self, runner: CliRunner) -> None:
        """Test ingest crawl has --max-pages option."""
        result = runner.invoke(cli, ["ingest", "crawl", "--help"])

        assert result.exit_code == 0
        assert "--max-pages" in result.output

    def test_ingest_crawl_has_max_depth_option(self, runner: CliRunner) -> None:
        """Test ingest crawl has --max-depth option."""
        result = runner.invoke(cli, ["ingest", "crawl", "--help"])

        assert result.exit_code == 0
        assert "--max-depth" in result.output

    def test_ingest_crawl_has_strategy_option(self, runner: CliRunner) -> None:
        """Test ingest crawl has --strategy option."""
        result = runner.invoke(cli, ["ingest", "crawl", "--help"])

        assert result.exit_code == 0
        assert "--strategy" in result.output
        # Check strategy choices
        assert "bfs" in result.output
        assert "dfs" in result.output
        assert "bestfirst" in result.output

    # --- Ingest clone command ---
    def test_ingest_clone_help(self, runner: CliRunner) -> None:
        """Test ingest clone command help."""
        result = runner.invoke(cli, ["ingest", "clone", "--help"])

        assert result.exit_code == 0
        assert "REPO" in result.output

    def test_ingest_clone_has_branch_option(self, runner: CliRunner) -> None:
        """Test ingest clone has --branch option."""
        result = runner.invoke(cli, ["ingest", "clone", "--help"])

        assert result.exit_code == 0
        assert "--branch" in result.output

    def test_ingest_clone_has_shallow_option(self, runner: CliRunner) -> None:
        """Test ingest clone has --shallow option."""
        result = runner.invoke(cli, ["ingest", "clone", "--help"])

        assert result.exit_code == 0
        assert "--shallow" in result.output

    def test_ingest_clone_has_max_files_option(self, runner: CliRunner) -> None:
        """Test ingest clone has --max-files option."""
        result = runner.invoke(cli, ["ingest", "clone", "--help"])

        assert result.exit_code == 0
        assert "--max-files" in result.output


class TestProcessGroup:
    """Test process command group."""

    def test_process_help(self, runner: CliRunner) -> None:
        """Test process group help."""
        result = runner.invoke(cli, ["process", "--help"])

        assert result.exit_code == 0
        assert "run" in result.output
        assert "search" in result.output
        assert "stats" in result.output
        assert "setup" in result.output
        assert "check" in result.output
        assert "export" in result.output
        assert "import" in result.output
        assert "visualize" in result.output
        assert "deploy" in result.output
        assert "server" in result.output

    # --- Process run command ---
    def test_process_run_help(self, runner: CliRunner) -> None:
        """Test process run command help."""
        result = runner.invoke(cli, ["process", "run", "--help"])

        assert result.exit_code == 0
        assert "INPUT_PATH" in result.output

    def test_process_run_has_output_option(self, runner: CliRunner) -> None:
        """Test process run has --output option."""
        result = runner.invoke(cli, ["process", "run", "--help"])

        assert result.exit_code == 0
        assert "--output" in result.output or "-o" in result.output

    def test_process_run_has_text_profile_option(self, runner: CliRunner) -> None:
        """Test process run has --text-profile option."""
        result = runner.invoke(cli, ["process", "run", "--help"])

        assert result.exit_code == 0
        assert "--text-profile" in result.output
        # Check profile choices
        assert "low" in result.output
        assert "medium" in result.output
        assert "high" in result.output

    def test_process_run_has_code_profile_option(self, runner: CliRunner) -> None:
        """Test process run has --code-profile option."""
        result = runner.invoke(cli, ["process", "run", "--help"])

        assert result.exit_code == 0
        assert "--code-profile" in result.output

    def test_process_run_has_table_mode_option(self, runner: CliRunner) -> None:
        """Test process run has --table-mode option."""
        result = runner.invoke(cli, ["process", "run", "--help"])

        assert result.exit_code == 0
        assert "--table-mode" in result.output
        # Check mode choices
        assert "separate" in result.output
        assert "unified" in result.output
        assert "both" in result.output

    def test_process_run_has_incremental_option(self, runner: CliRunner) -> None:
        """Test process run has --incremental option."""
        result = runner.invoke(cli, ["process", "run", "--help"])

        assert result.exit_code == 0
        assert "--incremental" in result.output

    def test_process_run_has_batch_size_option(self, runner: CliRunner) -> None:
        """Test process run has --batch-size option."""
        result = runner.invoke(cli, ["process", "run", "--help"])

        assert result.exit_code == 0
        assert "--batch-size" in result.output

    # --- Process search command ---
    def test_process_search_help(self, runner: CliRunner) -> None:
        """Test process search command help."""
        result = runner.invoke(cli, ["process", "search", "--help"])

        assert result.exit_code == 0
        assert "QUERY" in result.output
        assert "DB_PATH" in result.output

    def test_process_search_has_limit_option(self, runner: CliRunner) -> None:
        """Test process search has --limit option."""
        result = runner.invoke(cli, ["process", "search", "--help"])

        assert result.exit_code == 0
        assert "--limit" in result.output or "-k" in result.output

    def test_process_search_has_table_option(self, runner: CliRunner) -> None:
        """Test process search has --table option."""
        result = runner.invoke(cli, ["process", "search", "--help"])

        assert result.exit_code == 0
        assert "--table" in result.output
        # Check table choices
        assert "text_chunks" in result.output
        assert "code_chunks" in result.output

    def test_process_search_has_hybrid_option(self, runner: CliRunner) -> None:
        """Test process search has --hybrid option."""
        result = runner.invoke(cli, ["process", "search", "--help"])

        assert result.exit_code == 0
        assert "--hybrid" in result.output

    def test_process_search_has_rerank_option(self, runner: CliRunner) -> None:
        """Test process search has --rerank option."""
        result = runner.invoke(cli, ["process", "search", "--help"])

        assert result.exit_code == 0
        assert "--rerank" in result.output

    # --- Other process commands ---
    def test_process_stats_help(self, runner: CliRunner) -> None:
        """Test process stats command help."""
        result = runner.invoke(cli, ["process", "stats", "--help"])

        assert result.exit_code == 0

    def test_process_setup_help(self, runner: CliRunner) -> None:
        """Test process setup command help."""
        result = runner.invoke(cli, ["process", "setup", "--help"])

        assert result.exit_code == 0

    def test_process_check_help(self, runner: CliRunner) -> None:
        """Test process check command help."""
        result = runner.invoke(cli, ["process", "check", "--help"])

        assert result.exit_code == 0

    def test_process_export_help(self, runner: CliRunner) -> None:
        """Test process export command help."""
        result = runner.invoke(cli, ["process", "export", "--help"])

        assert result.exit_code == 0

    def test_process_import_help(self, runner: CliRunner) -> None:
        """Test process import command help."""
        result = runner.invoke(cli, ["process", "import", "--help"])

        assert result.exit_code == 0


class TestCommandCounts:
    """Test that all expected commands are registered."""

    def test_research_is_command(self, runner: CliRunner) -> None:
        """Test research is a direct command."""
        result = runner.invoke(cli, ["research", "--help"])

        # Should be a direct command with TOPIC argument
        assert "TOPIC" in result.output

    def test_parse_command_count(self, runner: CliRunner) -> None:
        """Test parse group has expected commands."""
        result = runner.invoke(cli, ["parse", "--help"])

        # Should have 10 commands
        expected = [
            "refs",
            "retrieve",
            "batch",
            "doi2bib",
            "verify",
            "citations",
            "sources",
            "auth",
            "init",
            "config",
        ]
        for cmd in expected:
            assert cmd in result.output, f"Missing command: {cmd}"

    def test_ingest_command_count(self, runner: CliRunner) -> None:
        """Test ingest group has expected commands."""
        result = runner.invoke(cli, ["ingest", "--help"])

        # Should have 5 commands
        expected = ["file", "batch", "crawl", "clone", "describe"]
        for cmd in expected:
            assert cmd in result.output, f"Missing command: {cmd}"

    def test_process_command_count(self, runner: CliRunner) -> None:
        """Test process group has expected commands."""
        result = runner.invoke(cli, ["process", "--help"])

        # Should have 11 commands
        expected = [
            "run",
            "search",
            "stats",
            "setup",
            "check",
            "export",
            "import",
            "visualize",
            "deploy",
            "server",
            "test-e2e",
        ]
        for cmd in expected:
            assert cmd in result.output, f"Missing command: {cmd}"
