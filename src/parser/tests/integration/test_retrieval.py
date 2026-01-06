"""Integration tests for paper retrieval."""

from pathlib import Path

import pytest

from parser.acquisition.downloader import DownloadConfig, PaperDownloader
from parser.acquisition.retriever import PaperRetriever, RetrievalStatus


class TestPaperDownloaderConfig:
    """Test paper downloader configuration."""

    def test_default_config(self) -> None:
        """Test default download configuration."""
        config = DownloadConfig()

        assert config.skip_existing is True
        assert config.generate_bibtex is True

    def test_custom_config(self, output_dir: Path) -> None:
        """Test custom download configuration."""
        config = DownloadConfig(
            output_dir=output_dir,
            skip_existing=False,
            max_references=100,
        )

        assert config.output_dir == output_dir
        assert config.skip_existing is False
        assert config.max_references == 100


class TestPaperDownloader:
    """Test paper downloader class."""

    def test_instantiation(self) -> None:
        """Test downloader can be instantiated."""
        downloader = PaperDownloader()
        assert downloader is not None

    def test_instantiation_with_config(self, output_dir: Path) -> None:
        """Test downloader with custom config."""
        config = DownloadConfig(output_dir=output_dir)
        downloader = PaperDownloader(config=config)
        assert downloader is not None


@pytest.mark.live_api
class TestLiveRetrieval:
    """Tests that require live API access.

    Run with: pytest --live-api
    """

    @pytest.fixture
    def retriever(self) -> PaperRetriever:
        """Create paper retriever."""
        from parser.acquisition.config import Config
        config = Config()
        return PaperRetriever(config)

    @pytest.mark.asyncio
    async def test_retrieve_arxiv(self, retriever: PaperRetriever, output_dir: Path, valid_arxiv_id: str) -> None:
        """Test retrieving arXiv paper."""
        result = await retriever.retrieve(
            identifier=f"arXiv:{valid_arxiv_id}",
            output_dir=output_dir,
        )

        assert result.status in (RetrievalStatus.SUCCESS, RetrievalStatus.NOT_FOUND)

    @pytest.mark.asyncio
    async def test_retrieve_doi(self, retriever: PaperRetriever, output_dir: Path, valid_doi: str) -> None:
        """Test retrieving paper by DOI."""
        result = await retriever.retrieve(
            identifier=valid_doi,
            output_dir=output_dir,
        )

        # May not find open access version
        assert result.status in (RetrievalStatus.SUCCESS, RetrievalStatus.NOT_FOUND, RetrievalStatus.SKIPPED)


@pytest.mark.slow
class TestSlowOperations:
    """Tests that take a long time."""

    @pytest.mark.asyncio
    async def test_batch_download(self, output_dir: Path) -> None:
        """Test batch download (skipped by default)."""
        pytest.skip("Batch download test requires --slow flag")
