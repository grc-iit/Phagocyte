"""Unit tests for reference parser."""

from pathlib import Path

import pytest

from parser.parser import ParsedReference, ReferenceType, ResearchParser


class TestReferenceType:
    """Test ReferenceType enum."""

    def test_all_types_defined(self) -> None:
        """Test all reference types are defined."""
        assert ReferenceType.GITHUB.value == "github"
        assert ReferenceType.ARXIV.value == "arxiv"
        assert ReferenceType.DOI.value == "doi"
        assert ReferenceType.PAPER.value == "paper"
        assert ReferenceType.BLOG.value == "blog"
        assert ReferenceType.PDF.value == "pdf"
        assert ReferenceType.YOUTUBE.value == "youtube"
        assert ReferenceType.PODCAST.value == "podcast"
        assert ReferenceType.BOOK.value == "book"
        assert ReferenceType.WEBSITE.value == "website"


class TestParsedReference:
    """Test ParsedReference dataclass."""

    def test_create_reference(self) -> None:
        """Test creating a parsed reference."""
        ref = ParsedReference(
            type=ReferenceType.GITHUB,
            value="huggingface/transformers",
            title="Transformers",
            url="https://github.com/huggingface/transformers",
        )

        assert ref.type == ReferenceType.GITHUB
        assert ref.value == "huggingface/transformers"
        assert ref.title == "Transformers"
        assert ref.url == "https://github.com/huggingface/transformers"

    def test_default_values(self) -> None:
        """Test default values."""
        ref = ParsedReference(type=ReferenceType.WEBSITE, value="example.com")

        assert ref.title == ""
        assert ref.authors == ""
        assert ref.year == ""
        assert ref.url is None
        assert ref.context == ""
        assert ref.metadata == {}


class TestResearchParserGitHub:
    """Test GitHub extraction."""

    @pytest.fixture
    def parser(self) -> ResearchParser:
        """Create parser instance."""
        return ResearchParser()

    def test_extract_github_backtick_format(
        self, parser: ResearchParser, sample_github_text: str
    ) -> None:
        """Test extracting GitHub repos from backtick format."""
        refs = parser.parse(sample_github_text)
        github_refs = [r for r in refs if r.type == ReferenceType.GITHUB]

        assert len(github_refs) >= 2
        values = [r.value for r in github_refs]
        assert "huggingface/transformers" in values

    def test_extract_github_url_format(self, parser: ResearchParser) -> None:
        """Test extracting GitHub repos from URLs."""
        text = "See https://github.com/pytorch/pytorch for details"
        refs = parser.parse(text)
        github_refs = [r for r in refs if r.type == ReferenceType.GITHUB]

        assert len(github_refs) >= 1
        assert any("pytorch/pytorch" in r.value for r in github_refs)

    def test_extract_repository_format(
        self, parser: ResearchParser, sample_github_text: str
    ) -> None:
        """Test extracting repos from **Repository:** format."""
        refs = parser.parse(sample_github_text)
        github_refs = [r for r in refs if r.type == ReferenceType.GITHUB]

        values = [r.value for r in github_refs]
        assert "openai/whisper" in values


class TestResearchParserArXiv:
    """Test arXiv extraction."""

    @pytest.fixture
    def parser(self) -> ResearchParser:
        """Create parser instance."""
        return ResearchParser()

    def test_extract_arxiv_id(
        self, parser: ResearchParser, sample_arxiv_text: str
    ) -> None:
        """Test extracting arXiv IDs."""
        refs = parser.parse(sample_arxiv_text)
        arxiv_refs = [r for r in refs if r.type == ReferenceType.ARXIV]

        assert len(arxiv_refs) >= 2
        values = [r.value for r in arxiv_refs]
        assert any("2005.14165" in v for v in values)

    def test_extract_arxiv_url(self, parser: ResearchParser) -> None:
        """Test extracting arXiv from URL."""
        text = "Paper at https://arxiv.org/abs/1810.04805"
        refs = parser.parse(text)
        arxiv_refs = [r for r in refs if r.type == ReferenceType.ARXIV]

        assert len(arxiv_refs) >= 1


class TestResearchParserDOI:
    """Test DOI extraction."""

    @pytest.fixture
    def parser(self) -> ResearchParser:
        """Create parser instance."""
        return ResearchParser()

    def test_extract_doi(self, parser: ResearchParser, sample_doi_text: str) -> None:
        """Test extracting DOIs."""
        refs = parser.parse(sample_doi_text)
        doi_refs = [r for r in refs if r.type == ReferenceType.DOI]

        assert len(doi_refs) >= 1

    def test_extract_doi_url(self, parser: ResearchParser) -> None:
        """Test extracting DOI from URL."""
        text = "Available at https://doi.org/10.1145/3442188.3445922"
        refs = parser.parse(text)
        doi_refs = [r for r in refs if r.type == ReferenceType.DOI]

        assert len(doi_refs) >= 1


class TestResearchParserYouTube:
    """Test YouTube extraction."""

    @pytest.fixture
    def parser(self) -> ResearchParser:
        """Create parser instance."""
        return ResearchParser()

    def test_extract_youtube_full_url(
        self, parser: ResearchParser, sample_youtube_text: str
    ) -> None:
        """Test extracting YouTube full URLs."""
        refs = parser.parse(sample_youtube_text)
        yt_refs = [r for r in refs if r.type == ReferenceType.YOUTUBE]

        assert len(yt_refs) >= 1

    def test_extract_youtube_short_url(self, parser: ResearchParser) -> None:
        """Test extracting YouTube short URLs."""
        text = "Watch: https://youtu.be/dQw4w9WgXcQ"
        refs = parser.parse(text)
        yt_refs = [r for r in refs if r.type == ReferenceType.YOUTUBE]

        assert len(yt_refs) >= 1


class TestResearchParserDeduplication:
    """Test reference deduplication."""

    @pytest.fixture
    def parser(self) -> ResearchParser:
        """Create parser instance."""
        return ResearchParser()

    def test_deduplicate_same_repo(self, parser: ResearchParser) -> None:
        """Test that duplicate repos are removed."""
        text = """
        Check `huggingface/transformers` and also
        github.com/huggingface/transformers for more info.
        """
        refs = parser.parse(text)
        github_refs = [r for r in refs if r.type == ReferenceType.GITHUB]

        # Should deduplicate
        transformers_refs = [r for r in github_refs if "transformers" in r.value]
        assert len(transformers_refs) == 1


class TestResearchParserFile:
    """Test file parsing."""

    @pytest.fixture
    def parser(self) -> ResearchParser:
        """Create parser instance."""
        return ResearchParser()

    def test_parse_markdown_file(
        self, parser: ResearchParser, tmp_path: Path, sample_research_text: str
    ) -> None:
        """Test parsing a markdown file."""
        md_file = tmp_path / "research.md"
        md_file.write_text(sample_research_text)

        refs = parser.parse_file(md_file)

        assert len(refs) > 0
        types = {r.type for r in refs}
        assert ReferenceType.GITHUB in types or ReferenceType.ARXIV in types

    def test_parse_json_file(self, parser: ResearchParser, tmp_path: Path) -> None:
        """Test parsing a JSON file."""
        import json

        json_file = tmp_path / "research.json"
        data = {"report": "Check github.com/pytorch/pytorch"}
        json_file.write_text(json.dumps(data))

        refs = parser.parse_file(json_file)
        github_refs = [r for r in refs if r.type == ReferenceType.GITHUB]

        assert len(github_refs) >= 1
