"""Unit tests for DOI to BibTeX module."""


from parser.doi2bib.metadata import Author, PaperMetadata
from parser.doi2bib.resolver import (
    IdentifierType,
    PaperIdentifier,
    resolve_identifier,
)


class TestIdentifierType:
    """Test IdentifierType enum."""

    def test_all_types_defined(self) -> None:
        """Test all identifier types are defined."""
        assert IdentifierType.DOI.value == "doi"
        assert IdentifierType.ARXIV.value == "arxiv"
        assert IdentifierType.PUBMED.value == "pubmed"
        assert IdentifierType.PDF_URL.value == "pdf_url"
        assert IdentifierType.TITLE.value == "title"
        assert IdentifierType.UNKNOWN.value == "unknown"


class TestPaperIdentifier:
    """Test PaperIdentifier dataclass."""

    def test_create_doi_identifier(self, valid_doi: str) -> None:
        """Test creating DOI identifier."""
        identifier = PaperIdentifier(
            original=valid_doi,
            type=IdentifierType.DOI,
            value=valid_doi,
        )

        assert identifier.type == IdentifierType.DOI
        assert identifier.value == valid_doi
        assert identifier.original == valid_doi

    def test_create_arxiv_identifier(self, valid_arxiv_id: str) -> None:
        """Test creating arXiv identifier."""
        identifier = PaperIdentifier(
            original=f"arXiv:{valid_arxiv_id}",
            type=IdentifierType.ARXIV,
            value=valid_arxiv_id,
        )

        assert identifier.type == IdentifierType.ARXIV
        assert identifier.value == valid_arxiv_id


class TestResolveIdentifier:
    """Test identifier resolution."""

    def test_resolve_doi(self, valid_doi: str) -> None:
        """Test resolving DOI string."""
        result = resolve_identifier(valid_doi)

        assert result.type == IdentifierType.DOI
        assert valid_doi in result.value

    def test_resolve_arxiv_with_prefix(self, valid_arxiv_id: str) -> None:
        """Test resolving arXiv ID with prefix."""
        result = resolve_identifier(f"arXiv:{valid_arxiv_id}")

        assert result.type == IdentifierType.ARXIV
        assert valid_arxiv_id in result.value

    def test_resolve_arxiv_without_prefix(self, valid_arxiv_id: str) -> None:
        """Test resolving arXiv ID without prefix."""
        result = resolve_identifier(valid_arxiv_id)

        # Should detect as arXiv based on format
        assert result.type == IdentifierType.ARXIV

    def test_resolve_doi_url(self, valid_doi: str) -> None:
        """Test resolving DOI URL."""
        result = resolve_identifier(f"https://doi.org/{valid_doi}")

        assert result.type == IdentifierType.DOI
        assert valid_doi in result.value

    def test_resolve_arxiv_url(self, valid_arxiv_id: str) -> None:
        """Test resolving arXiv URL."""
        result = resolve_identifier(f"https://arxiv.org/abs/{valid_arxiv_id}")

        assert result.type == IdentifierType.ARXIV

    def test_resolve_unknown(self) -> None:
        """Test resolving unknown string as title search."""
        result = resolve_identifier("Attention Is All You Need")

        assert result.type == IdentifierType.TITLE


class TestAuthor:
    """Test Author dataclass."""

    def test_author_full_name(self) -> None:
        """Test author name property."""
        author = Author(name="John Doe", given="John", family="Doe")

        assert author.name == "John Doe"
        assert author.given == "John"
        assert author.family == "Doe"

    def test_author_affiliation(self) -> None:
        """Test author with affiliations."""
        author = Author(
            name="Jane Smith",
            given="Jane",
            family="Smith",
            affiliations=["MIT"],
        )

        assert author.affiliations == ["MIT"]


class TestPaperMetadata:
    """Test PaperMetadata dataclass."""

    def test_metadata_creation(self) -> None:
        """Test creating paper metadata."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=[Author(name="John Doe", given="John", family="Doe")],
            doi="10.1234/test",
            year=2023,
        )

        assert metadata.title == "Test Paper"
        assert len(metadata.authors) == 1
        assert metadata.doi == "10.1234/test"
        assert metadata.year == 2023

    def test_metadata_optional_fields(self) -> None:
        """Test metadata with optional fields."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=[],
        )

        assert metadata.doi is None
        assert metadata.arxiv_id is None
        assert metadata.abstract is None
        assert metadata.year is None
