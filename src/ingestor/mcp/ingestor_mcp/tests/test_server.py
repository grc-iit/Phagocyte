"""Unit tests for ingestor MCP server."""


from ingestor_mcp.server import (
    BatchInput,
    BatchResult,
    CloneRepoInput,
    CrawlInput,
    CrawlResult,
    GitHubInput,
    GitHubResult,
    IngestInput,
    IngestResult,
    SupportedFormats,
    YouTubeInput,
    YouTubeResult,
)


class TestIngestInput:
    """Test IngestInput model."""

    def test_default_values(self) -> None:
        """Test default input values."""
        input = IngestInput(input_path="/path/to/file.pdf")

        assert input.input_path == "/path/to/file.pdf"
        assert input.output_dir == "./output"
        assert input.keep_raw_images is False
        assert input.img_format == "png"
        assert input.generate_metadata is False
        assert input.describe_images is False
        assert input.verbose is False

    def test_custom_values(self) -> None:
        """Test custom input values."""
        input = IngestInput(
            input_path="/path/to/doc.docx",
            output_dir="/custom/output",
            keep_raw_images=True,
            img_format="jpg",
            describe_images=True,
            verbose=True,
        )

        assert input.output_dir == "/custom/output"
        assert input.keep_raw_images is True
        assert input.img_format == "jpg"


class TestIngestResult:
    """Test IngestResult model."""

    def test_success_result(self) -> None:
        """Test successful ingestion result."""
        result = IngestResult(
            success=True,
            output_path="/output/file.md",
            source="/input/file.pdf",
            media_type="pdf",
            image_count=5,
        )

        assert result.success is True
        assert result.output_path is not None
        assert result.image_count == 5

    def test_failed_result(self) -> None:
        """Test failed ingestion result."""
        result = IngestResult(
            success=False,
            source="/input/file.xyz",
            error="Unsupported format",
        )

        assert result.success is False
        assert result.error == "Unsupported format"


class TestCrawlInput:
    """Test CrawlInput model."""

    def test_default_values(self) -> None:
        """Test default crawl values."""
        input = CrawlInput(url="https://example.com")

        assert input.url == "https://example.com"
        assert input.strategy == "bfs"
        assert input.max_depth == 2
        assert input.max_pages == 50
        assert input.domain_only is True

    def test_strategies(self) -> None:
        """Test crawl strategy options."""
        for strategy in ["bfs", "dfs", "bestfirst"]:
            input = CrawlInput(url="https://test.com", strategy=strategy)
            assert input.strategy == strategy

    def test_patterns(self) -> None:
        """Test URL patterns."""
        input = CrawlInput(
            url="https://docs.example.com",
            include_patterns=["/api/*", "/guide/*"],
            exclude_patterns=["/old/*"],
        )

        assert len(input.include_patterns) == 2
        assert len(input.exclude_patterns) == 1


class TestCrawlResult:
    """Test CrawlResult model."""

    def test_crawl_stats(self) -> None:
        """Test crawl result statistics."""
        result = CrawlResult(
            success=True,
            pages_crawled=25,
            output_dir="/output/crawl",
            files_created=["page1.md", "page2.md"],
        )

        assert result.pages_crawled == 25
        assert len(result.files_created) == 2


class TestYouTubeInput:
    """Test YouTubeInput model."""

    def test_default_values(self) -> None:
        """Test default YouTube values."""
        input = YouTubeInput(url="https://youtube.com/watch?v=abc123")

        assert input.url == "https://youtube.com/watch?v=abc123"
        assert input.captions == "auto"
        assert input.include_playlist is False

    def test_caption_options(self) -> None:
        """Test caption preference options."""
        for captions in ["auto", "manual", "any"]:
            input = YouTubeInput(url="https://youtube.com/watch?v=test", captions=captions)
            assert input.captions == captions


class TestYouTubeResult:
    """Test YouTubeResult model."""

    def test_video_result(self) -> None:
        """Test video result."""
        result = YouTubeResult(
            success=True,
            output_path="/output/video.md",
            video_title="Test Video",
            duration="10:25",
        )

        assert result.success is True
        assert result.video_title == "Test Video"


class TestGitHubInput:
    """Test GitHubInput model."""

    def test_default_values(self) -> None:
        """Test default GitHub values."""
        input = GitHubInput(url="https://github.com/owner/repo")

        assert input.url == "https://github.com/owner/repo"
        assert input.branch == "main"
        assert len(input.include_patterns) > 0
        assert len(input.exclude_patterns) > 0

    def test_custom_patterns(self) -> None:
        """Test custom file patterns."""
        input = GitHubInput(
            url="https://github.com/owner/repo",
            include_patterns=["*.rs", "*.toml"],
            exclude_patterns=["target/*"],
        )

        assert "*.rs" in input.include_patterns


class TestGitHubResult:
    """Test GitHubResult model."""

    def test_repo_result(self) -> None:
        """Test repository result."""
        result = GitHubResult(
            success=True,
            output_dir="/output/repo",
            repo_name="owner/repo",
            files_processed=100,
        )

        assert result.success is True
        assert result.files_processed == 100


class TestBatchInput:
    """Test BatchInput model."""

    def test_default_values(self) -> None:
        """Test default batch values."""
        input = BatchInput(input_dir="/path/to/docs")

        assert input.input_dir == "/path/to/docs"
        assert input.recursive is True
        assert input.concurrency == 5

    def test_concurrency_limits(self) -> None:
        """Test concurrency limits."""
        input = BatchInput(input_dir="/docs", concurrency=20)
        assert input.concurrency == 20


class TestBatchResult:
    """Test BatchResult model."""

    def test_batch_stats(self) -> None:
        """Test batch result statistics."""
        result = BatchResult(
            success=True,
            total_files=100,
            processed=95,
            failed=5,
            output_dir="/output",
        )

        assert result.total_files == 100
        assert result.processed == 95
        assert result.failed == 5


class TestCloneRepoInput:
    """Test CloneRepoInput model."""

    def test_default_values(self) -> None:
        """Test default clone values."""
        input = CloneRepoInput(repo="https://github.com/owner/repo")

        assert input.repo == "https://github.com/owner/repo"
        assert input.shallow is True
        assert input.depth == 1

    def test_clone_options(self) -> None:
        """Test clone options."""
        input = CloneRepoInput(
            repo="git@github.com:owner/repo.git",
            branch="develop",
            shallow=False,
            token="secret",
        )

        assert input.branch == "develop"
        assert input.shallow is False


class TestSupportedFormats:
    """Test SupportedFormats model."""

    def test_format_lists(self) -> None:
        """Test supported format lists."""
        formats = SupportedFormats(
            documents=["pdf", "docx", "pptx"],
            spreadsheets=["xlsx", "csv"],
            web=["html"],
            code=["py", "js", "ts"],
            data=["json", "yaml"],
            audio=["mp3", "wav"],
        )

        assert "pdf" in formats.documents
        assert "xlsx" in formats.spreadsheets
        assert "py" in formats.code


class TestMCPTools:
    """Test MCP tool registration."""

    def test_server_instantiation(self) -> None:
        """Test MCP server can be imported."""
        from ingestor_mcp.server import mcp

        assert mcp is not None
        assert mcp.name == "ingestor-mcp"

    def test_tools_registered(self) -> None:
        """Test key tools are registered."""
        from ingestor_mcp.server import (
            batch_ingest,
            crawl_website,
            ingest_file,
            ingest_github,
            ingest_youtube,
        )

        assert ingest_file is not None
        assert crawl_website is not None
        assert ingest_youtube is not None
        assert ingest_github is not None
        assert batch_ingest is not None
