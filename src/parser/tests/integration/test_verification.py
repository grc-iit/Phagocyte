"""Integration tests for citation verification."""

from pathlib import Path

import pytest

from parser.doi2bib.verifier import CitationVerifier, parse_bib_file


class TestEndToEndVerification:
    """Test end-to-end citation verification workflow."""

    @pytest.fixture
    def verifier(self) -> CitationVerifier:
        """Create verifier instance."""
        return CitationVerifier()

    def test_verify_from_bib_file(
        self, verifier: CitationVerifier, tmp_path: Path, sample_bibtex: str
    ) -> None:
        """Test verifying citations from BibTeX file."""
        bib_file = tmp_path / "refs.bib"
        bib_file.write_text(sample_bibtex)

        entries = parse_bib_file(bib_file)
        assert len(entries) > 0


@pytest.mark.live_api
class TestLiveVerification:
    """Tests that require live API access.

    Run with: pytest --live-api
    """

    @pytest.fixture
    def verifier(self) -> CitationVerifier:
        """Create verifier instance."""
        return CitationVerifier()

    @pytest.mark.asyncio
    async def test_verify_known_paper(self, verifier: CitationVerifier) -> None:
        """Test verifying a known paper."""
        # Attention Is All You Need is well-known
        result = await verifier.verify_by_title("Attention Is All You Need")

        # Should find the paper
        assert result is not None
