"""Unit tests for citation verifier."""

from pathlib import Path

import pytest

from parser.doi2bib.verifier import (
    BibEntry,
    CitationVerifier,
    VerificationResult,
    VerificationStats,
    parse_bib_file,
)


class TestBibEntry:
    """Test BibEntry dataclass."""

    def test_create_entry(self) -> None:
        """Test creating a BibTeX entry."""
        raw_bib = """@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam},
  year={2017}
}"""
        entry = BibEntry(
            key="vaswani2017attention",
            entry_type="article",
            raw=raw_bib,
            title="Attention is all you need",
            author="Vaswani, Ashish and Shazeer, Noam",
        )

        assert entry.key == "vaswani2017attention"
        assert entry.entry_type == "article"
        assert entry.title == "Attention is all you need"

    def test_entry_with_doi(self) -> None:
        """Test entry with DOI."""
        raw_bib = "@article{test, title={Test}, doi={10.1234/test}}"
        entry = BibEntry(
            key="test",
            entry_type="article",
            raw=raw_bib,
            title="Test",
            doi="10.1234/test",
        )

        assert entry.doi == "10.1234/test"

    def test_parse_entry(self) -> None:
        """Test parsing raw BibTeX entry."""
        raw_bib = """@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam},
  doi={10.5555/3295222.3295349},
  year={2017}
}"""
        entry = BibEntry.parse(raw_bib)

        assert entry is not None
        assert entry.key == "vaswani2017attention"
        assert entry.entry_type == "article"
        assert entry.doi == "10.5555/3295222.3295349"


class TestParseBibFile:
    """Test BibTeX file parsing."""

    def test_parse_valid_bib(self, tmp_path: Path, sample_bibtex: str) -> None:
        """Test parsing valid BibTeX file."""
        bib_file = tmp_path / "refs.bib"
        bib_file.write_text(sample_bibtex)

        entries = parse_bib_file(bib_file)

        assert len(entries) == 2
        keys = [e.key for e in entries]
        assert "vaswani2017attention" in keys
        assert "devlin2019bert" in keys

    def test_parse_empty_file(self, tmp_path: Path) -> None:
        """Test parsing empty BibTeX file."""
        bib_file = tmp_path / "empty.bib"
        bib_file.write_text("")

        entries = parse_bib_file(bib_file)
        assert len(entries) == 0


class TestVerificationResult:
    """Test VerificationResult dataclass."""

    def test_verified_result(self) -> None:
        """Test verified citation result."""
        result = VerificationResult(
            key="test",
            status="verified",
            bibtex="@article{test, title={Test}}",
            message="DOI verified via CrossRef",
        )

        assert result.status == "verified"
        assert "test" in result.key

    def test_unverified_result(self) -> None:
        """Test unverified citation result."""
        result = VerificationResult(
            key="test",
            status="failed",
            bibtex="@article{test, title={Unknown}}",
            message="No match found",
        )

        assert result.status == "failed"
        assert "No match found" in result.message


class TestVerificationStats:
    """Test VerificationStats."""

    def test_stats_defaults(self) -> None:
        """Test verification statistics defaults."""
        stats = VerificationStats()

        assert stats.verified == 0
        assert stats.failed == 0
        assert stats.total == 0

    def test_stats_calculation(self) -> None:
        """Test verification statistics calculation."""
        stats = VerificationStats(
            verified=5,
            arxiv=3,
            searched=1,
            website=1,
            failed=2,
        )

        assert stats.total_verified == 10  # 5+3+1+1
        assert stats.total == 12  # 10+2


class TestCitationVerifier:
    """Test CitationVerifier class."""

    @pytest.fixture
    def verifier(self) -> CitationVerifier:
        """Create verifier instance."""
        return CitationVerifier()

    def test_verifier_instantiation(self, verifier: CitationVerifier) -> None:
        """Test verifier can be instantiated."""
        assert verifier is not None
