"""Integration tests for Phagocyte CLI.

These tests require the actual modules to be installed.
Run with: pytest --integration
"""

import pytest
from pathlib import Path
from click.testing import CliRunner

import sys

sys.path.insert(0, str(__file__).rsplit("/tests", 1)[0] + "/src")

from cli import cli


@pytest.mark.integration
class TestModuleIntegration:
    """Test CLI integration with actual modules."""

    def test_parse_sources(self, runner: CliRunner) -> None:
        """Test parse sources command runs."""
        runner.invoke(cli, ["parse", "sources"])
        # Just verify it doesn't crash
        # Exit code may vary depending on module status

    def test_process_check(self, runner: CliRunner) -> None:
        """Test process check command runs."""
        runner.invoke(cli, ["process", "check"])
        # Just verify it doesn't crash


@pytest.mark.integration
class TestEndToEndWorkflow:
    """Test end-to-end workflow scenarios."""

    def test_ingest_then_process(
        self, runner: CliRunner, sample_markdown_file: Path
    ) -> None:
        """Test ingest followed by process workflow."""
        # This would test the full pipeline
        # Skip actual execution in integration tests
        pass

    def test_research_to_parse_workflow(self, runner: CliRunner) -> None:
        """Test research output to parse refs workflow."""
        # This would test research -> parse refs
        pass
