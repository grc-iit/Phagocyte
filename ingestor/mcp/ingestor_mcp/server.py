"""MCP Server for document ingestion and media conversion operations.

This server exposes tools for:
- Converting documents (PDF, DOCX, PPTX, etc.) to Markdown
- Crawling websites to Markdown
- Processing YouTube videos (transcripts)
- Ingesting GitHub repositories
- Batch processing directories

Usage:
    uv run ingestor-mcp
"""

import asyncio
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize MCP server
mcp = FastMCP(
    name="ingestor-mcp",
    instructions="""
Ingestor MCP Server

Comprehensive media-to-markdown ingestion for LLM RAG and fine-tuning.

Supported formats:
- Documents: PDF, DOCX, PPTX, EPUB, TXT, Markdown
- Spreadsheets: XLSX, XLS, CSV
- Web: Websites (with deep crawling), YouTube videos
- Code: GitHub repositories, local codebases
- Data: JSON, XML, YAML
- Audio: MP3, WAV (requires Whisper)

Features:
- AI-powered file type detection (Google Magika)
- Image extraction and optional VLM descriptions
- Recursive directory processing
- Web crawling with depth control

Workflow:
1. ingest_file - Convert a single file to Markdown
2. crawl_website - Deep crawl a website
3. ingest_youtube - Get YouTube video transcript
4. ingest_github - Clone and convert a GitHub repo
5. batch_ingest - Process entire directories
"""
)


# =============================================================================
# Tool Input/Output Models
# =============================================================================


class IngestInput(BaseModel):
    """Input for file ingestion."""

    input_path: str = Field(description="File path or URL to ingest")
    output_dir: str = Field(default="./output", description="Output directory")
    keep_raw_images: bool = Field(default=False, description="Keep original image formats")
    img_format: str = Field(default="png", description="Target image format")
    generate_metadata: bool = Field(default=False, description="Generate JSON metadata")
    describe_images: bool = Field(default=False, description="Generate VLM descriptions (requires Ollama)")
    verbose: bool = Field(default=False, description="Verbose output")


class IngestResult(BaseModel):
    """Result of ingestion operation."""

    success: bool
    output_path: str | None = None
    source: str
    media_type: str | None = None
    image_count: int = 0
    error: str | None = None


class CrawlInput(BaseModel):
    """Input for website crawling."""

    url: str = Field(description="Starting URL to crawl")
    output_dir: str = Field(default="./output", description="Output directory")
    strategy: Literal["bfs", "dfs", "bestfirst"] = Field(
        default="bfs", description="Crawl strategy"
    )
    max_depth: int = Field(default=2, ge=0, le=10, description="Maximum crawl depth")
    max_pages: int = Field(default=50, ge=1, le=500, description="Maximum pages to crawl")
    include_patterns: list[str] = Field(default_factory=list, description="URL patterns to include")
    exclude_patterns: list[str] = Field(default_factory=list, description="URL patterns to exclude")
    domain_only: bool = Field(default=True, description="Stay within same domain")
    verbose: bool = Field(default=False, description="Verbose output")


class CrawlResult(BaseModel):
    """Result of crawl operation."""

    success: bool
    pages_crawled: int
    output_dir: str | None = None
    files_created: list[str] = Field(default_factory=list)
    error: str | None = None


class YouTubeInput(BaseModel):
    """Input for YouTube ingestion."""

    url: str = Field(description="YouTube video or playlist URL")
    output_dir: str = Field(default="./output", description="Output directory")
    captions: Literal["auto", "manual", "any"] = Field(
        default="auto", description="Caption preference"
    )
    include_playlist: bool = Field(default=False, description="Process entire playlist")
    verbose: bool = Field(default=False, description="Verbose output")


class YouTubeResult(BaseModel):
    """Result of YouTube ingestion."""

    success: bool
    output_path: str | None = None
    video_title: str | None = None
    duration: str | None = None
    videos_processed: int = 1
    error: str | None = None


class GitHubInput(BaseModel):
    """Input for GitHub ingestion."""

    url: str = Field(description="GitHub repository URL")
    output_dir: str = Field(default="./output", description="Output directory")
    branch: str = Field(default="main", description="Branch to clone")
    include_patterns: list[str] = Field(
        default_factory=lambda: ["*.py", "*.js", "*.ts", "*.md", "*.rst"],
        description="File patterns to include"
    )
    exclude_patterns: list[str] = Field(
        default_factory=lambda: ["node_modules/*", "__pycache__/*", ".git/*"],
        description="File patterns to exclude"
    )
    verbose: bool = Field(default=False, description="Verbose output")


class GitHubResult(BaseModel):
    """Result of GitHub ingestion."""

    success: bool
    output_dir: str | None = None
    repo_name: str | None = None
    files_processed: int = 0
    error: str | None = None


class BatchInput(BaseModel):
    """Input for batch ingestion."""

    input_dir: str = Field(description="Directory to process")
    output_dir: str = Field(default="./output", description="Output directory")
    recursive: bool = Field(default=True, description="Process subdirectories")
    concurrency: int = Field(default=5, ge=1, le=20, description="Max concurrent extractions")
    describe_images: bool = Field(default=False, description="Generate VLM descriptions")
    verbose: bool = Field(default=False, description="Verbose output")


class BatchResult(BaseModel):
    """Result of batch ingestion."""

    success: bool
    total_files: int
    processed: int
    failed: int
    output_dir: str | None = None
    results: list[dict] = Field(default_factory=list)


class SupportedFormats(BaseModel):
    """Supported file formats."""

    documents: list[str]
    spreadsheets: list[str]
    web: list[str]
    code: list[str]
    data: list[str]
    audio: list[str]


class CloneRepoInput(BaseModel):
    """Input for git repository cloning."""

    repo: str = Field(description="Repository URL (HTTPS/SSH) or local path")
    output_dir: str = Field(default="./output", description="Output directory")
    shallow: bool = Field(default=True, description="Use shallow clone")
    depth: int = Field(default=1, ge=1, description="Clone depth for shallow clones")
    branch: str | None = Field(default=None, description="Clone specific branch")
    tag: str | None = Field(default=None, description="Clone specific tag")
    commit: str | None = Field(default=None, description="Checkout specific commit")
    token: str | None = Field(default=None, description="Git token for private repos")
    submodules: bool = Field(default=False, description="Include git submodules")
    max_files: int = Field(default=500, ge=1, le=5000, description="Maximum files to process")
    max_file_size: int = Field(default=500000, ge=1000, description="Maximum file size in bytes")
    include_binary: bool = Field(default=False, description="Include binary file metadata")
    verbose: bool = Field(default=False, description="Verbose output")


class CloneRepoResult(BaseModel):
    """Result of git clone operation."""

    success: bool
    output_path: str | None = None
    repo_name: str | None = None
    files_processed: int = 0
    files_skipped: int = 0
    image_count: int = 0
    error: str | None = None


class DescribeImagesInput(BaseModel):
    """Input for VLM image description."""

    input_path: str = Field(description="Image file or directory of images")
    vlm_model: str = Field(default="llava:7b", description="VLM model for descriptions")
    ollama_host: str = Field(default="http://localhost:11434", description="Ollama server URL")
    output_file: str | None = Field(default=None, description="Optional output file for descriptions")
    verbose: bool = Field(default=False, description="Verbose output")


class DescribeImagesResult(BaseModel):
    """Result of VLM image description."""

    success: bool
    images_processed: int = 0
    descriptions: list[dict] = Field(default_factory=list)
    output_file: str | None = None
    error: str | None = None


class AudioTranscribeInput(BaseModel):
    """Input for audio transcription."""

    input_path: str = Field(description="Audio file path")
    output_dir: str = Field(default="./output", description="Output directory")
    whisper_model: str = Field(default="turbo", description="Whisper model (tiny, base, small, medium, large, turbo)")
    language: str | None = Field(default=None, description="Force language (auto-detect if not set)")
    verbose: bool = Field(default=False, description="Verbose output")


class AudioTranscribeResult(BaseModel):
    """Result of audio transcription."""

    success: bool
    output_path: str | None = None
    duration: str | None = None
    language: str | None = None
    error: str | None = None


# =============================================================================
# Tools
# =============================================================================


@mcp.tool()
async def ingest_file(input: IngestInput) -> IngestResult:
    """Convert a file or URL to Markdown.

    Supports documents, spreadsheets, ebooks, and more.
    Automatically detects file type using AI-powered detection.

    Args:
        input: Ingestion configuration

    Returns:
        Result with output path and metadata

    Example:
        ingest_file(input_path="./paper.pdf", output_dir="./markdown")
        ingest_file(input_path="./presentation.pptx", describe_images=True)
    """
    from ingestor.core import Router
    from ingestor.output.writer import OutputWriter
    from ingestor.types import IngestConfig

    config = IngestConfig(
        output_dir=Path(input.output_dir),
        keep_raw_images=input.keep_raw_images,
        target_image_format=input.img_format,
        generate_metadata=input.generate_metadata,
        verbose=input.verbose,
        describe_images=input.describe_images,
    )

    registry = _create_registry()
    router = Router(registry, config)
    writer = OutputWriter(config)

    try:
        if not router.can_process(input.input_path):
            media_type = router.detect_type(input.input_path)
            return IngestResult(
                success=False,
                source=input.input_path,
                media_type=media_type.value if media_type else None,
                error=f"No extractor available for this file type: {media_type.value if media_type else 'unknown'}",
            )

        result = await router.process(input.input_path)
        output_path = await writer.write(result)

        return IngestResult(
            success=True,
            output_path=str(output_path),
            source=input.input_path,
            media_type=result.media_type.value if result.media_type else None,
            image_count=result.image_count if result.has_images else 0,
        )

    except Exception as e:
        return IngestResult(
            success=False,
            source=input.input_path,
            error=str(e),
        )


@mcp.tool()
async def crawl_website(input: CrawlInput) -> CrawlResult:
    """Deep crawl a website and convert pages to Markdown.

    Crawls the URL and all linked pages up to max_depth.
    Supports BFS, DFS, and best-first crawl strategies.

    Args:
        input: Crawl configuration

    Returns:
        Result with crawl statistics

    Example:
        crawl_website(url="https://docs.example.com", max_depth=2, max_pages=100)
    """
    from ingestor.output.writer import OutputWriter
    from ingestor.types import IngestConfig, MediaType

    config = IngestConfig(
        output_dir=Path(input.output_dir),
        verbose=input.verbose,
        crawl_strategy=input.strategy,
        crawl_max_depth=input.max_depth,
        crawl_max_pages=input.max_pages,
    )

    registry = _create_registry()
    writer = OutputWriter(config)

    # Get web extractor
    extractor = registry.get(MediaType.WEB)
    if extractor is None:
        return CrawlResult(
            success=False,
            pages_crawled=0,
            error="Web extractor not available. Install with: uv sync --extra web",
        )

    try:
        files_created = []
        pages_crawled = 0

        # Configure crawl settings
        crawl_config = {
            "strategy": input.strategy,
            "max_depth": input.max_depth,
            "max_pages": input.max_pages,
            "include_patterns": input.include_patterns,
            "exclude_patterns": input.exclude_patterns,
            "same_domain": input.domain_only,
        }

        async for result in extractor.crawl(input.url, **crawl_config):
            output_path = await writer.write(result)
            files_created.append(str(output_path))
            pages_crawled += 1

        return CrawlResult(
            success=True,
            pages_crawled=pages_crawled,
            output_dir=input.output_dir,
            files_created=files_created[:20],  # Limit for response size
        )

    except Exception as e:
        return CrawlResult(
            success=False,
            pages_crawled=0,
            error=str(e),
        )


@mcp.tool()
async def ingest_youtube(input: YouTubeInput) -> YouTubeResult:
    """Get transcript from a YouTube video.

    Extracts captions/transcripts from YouTube videos.
    Supports auto-generated and manual captions.

    Args:
        input: YouTube ingestion configuration

    Returns:
        Result with transcript path

    Example:
        ingest_youtube(url="https://youtube.com/watch?v=...")
    """
    from ingestor.output.writer import OutputWriter
    from ingestor.types import IngestConfig, MediaType

    config = IngestConfig(
        output_dir=Path(input.output_dir),
        verbose=input.verbose,
        youtube_captions=input.captions,
        youtube_playlist=input.include_playlist,
    )

    registry = _create_registry()
    writer = OutputWriter(config)

    # Get YouTube extractor
    extractor = registry.get(MediaType.YOUTUBE)
    if extractor is None:
        return YouTubeResult(
            success=False,
            error="YouTube extractor not available. Install with: uv sync --extra youtube",
        )

    try:
        result = await extractor.extract(input.url, config)
        output_path = await writer.write(result)

        return YouTubeResult(
            success=True,
            output_path=str(output_path),
            video_title=result.title,
            duration=result.metadata.get("duration") if result.metadata else None,
        )

    except Exception as e:
        return YouTubeResult(
            success=False,
            error=str(e),
        )


@mcp.tool()
async def ingest_github(input: GitHubInput) -> GitHubResult:
    """Clone and convert a GitHub repository to Markdown.

    Clones the repository and converts code files to structured Markdown
    with syntax highlighting and file organization.

    Args:
        input: GitHub ingestion configuration

    Returns:
        Result with repository information

    Example:
        ingest_github(url="https://github.com/user/repo", branch="main")
    """
    from ingestor.output.writer import OutputWriter
    from ingestor.types import IngestConfig, MediaType

    config = IngestConfig(
        output_dir=Path(input.output_dir),
        verbose=input.verbose,
    )

    registry = _create_registry()
    writer = OutputWriter(config)

    # Get GitHub extractor
    extractor = registry.get(MediaType.GIT)
    if extractor is None:
        return GitHubResult(
            success=False,
            error="Git extractor not available",
        )

    try:
        # Configure extraction
        extract_config = {
            "branch": input.branch,
            "include_patterns": input.include_patterns,
            "exclude_patterns": input.exclude_patterns,
        }

        result = await extractor.extract(input.url, config, **extract_config)
        output_path = await writer.write(result)

        # Extract repo name from URL
        repo_name = input.url.rstrip("/").split("/")[-1].replace(".git", "")

        return GitHubResult(
            success=True,
            output_dir=str(output_path.parent if output_path else input.output_dir),
            repo_name=repo_name,
            files_processed=result.metadata.get("files_processed", 0) if result.metadata else 0,
        )

    except Exception as e:
        return GitHubResult(
            success=False,
            error=str(e),
        )


@mcp.tool()
async def batch_ingest(input: BatchInput) -> BatchResult:
    """Process all supported files in a directory.

    Recursively processes files and converts to Markdown.
    Also processes .url files containing URLs to crawl.

    Args:
        input: Batch ingestion configuration

    Returns:
        Summary of batch processing

    Example:
        batch_ingest(input_dir="./documents", recursive=True, concurrency=5)
    """
    from ingestor.core import Router
    from ingestor.output.writer import OutputWriter
    from ingestor.types import IngestConfig

    config = IngestConfig(
        output_dir=Path(input.output_dir),
        verbose=input.verbose,
        describe_images=input.describe_images,
    )

    registry = _create_registry()
    router = Router(registry, config)
    writer = OutputWriter(config)

    input_path = Path(input.input_dir)
    if not input_path.exists():
        return BatchResult(
            success=False,
            total_files=0,
            processed=0,
            failed=0,
            error=f"Directory not found: {input.input_dir}",
        )

    results = []
    processed = 0
    failed = 0

    try:
        async for result in router.process_directory(
            str(input_path),
            recursive=input.recursive,
            concurrency=input.concurrency
        ):
            try:
                output_path = await writer.write(result)
                processed += 1
                results.append({
                    "source": result.source,
                    "output": str(output_path),
                    "status": "success",
                })
            except Exception as e:
                failed += 1
                results.append({
                    "source": result.source,
                    "status": "failed",
                    "error": str(e),
                })

        return BatchResult(
            success=True,
            total_files=processed + failed,
            processed=processed,
            failed=failed,
            output_dir=input.output_dir,
            results=results[:50],  # Limit for response size
        )

    except Exception as e:
        return BatchResult(
            success=False,
            total_files=0,
            processed=processed,
            failed=failed,
            error=str(e),
        )


@mcp.tool()
async def list_supported_formats() -> SupportedFormats:
    """List all supported file formats.

    Returns categorized list of file formats that can be ingested.

    Returns:
        Supported formats by category
    """
    return SupportedFormats(
        documents=["pdf", "docx", "doc", "pptx", "ppt", "epub", "txt", "md", "rst", "rtf"],
        spreadsheets=["xlsx", "xls", "csv", "tsv"],
        web=["html", "htm", "url (website crawling)", "youtube"],
        code=["py", "js", "ts", "java", "cpp", "c", "go", "rs", "rb", "php", "github"],
        data=["json", "xml", "yaml", "yml", "toml"],
        audio=["mp3", "wav", "m4a", "flac", "ogg"],
    )


@mcp.tool()
async def detect_file_type(file_path: str) -> dict:
    """Detect the type of a file using AI-powered detection.

    Uses Google Magika for accurate file type detection
    regardless of file extension.

    Args:
        file_path: Path to the file

    Returns:
        Detected file type information
    """
    from ingestor.core.detector import FileDetector
    from ingestor.types import MediaType

    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    detector = FileDetector()
    media_type = detector.detect(path)

    return {
        "file_path": file_path,
        "media_type": media_type.value if media_type else "unknown",
        "extension": path.suffix,
        "can_process": media_type != MediaType.UNKNOWN if media_type else False,
    }


@mcp.tool()
async def clone_repo(input: CloneRepoInput) -> CloneRepoResult:
    """Clone and ingest a git repository with advanced options.

    Supports HTTPS URLs, SSH URLs, local paths, and .download_git files.
    Provides fine-grained control over clone depth, branches, tags, and file limits.

    Args:
        input: Clone configuration

    Returns:
        Result with repository information and statistics

    Example:
        clone_repo(repo="https://github.com/pallets/flask", shallow=True)
        clone_repo(repo="git@github.com:user/private.git", token="ghp_xxx")
        clone_repo(repo="https://github.com/user/repo", branch="develop", max_files=200)
    """
    from ingestor.output.writer import OutputWriter
    from ingestor.types import IngestConfig

    config = IngestConfig(
        output_dir=Path(input.output_dir),
        verbose=input.verbose,
    )

    try:
        from ingestor.extractors.git.git_extractor import GitExtractor, GitRepoConfig
    except ImportError:
        return CloneRepoResult(
            success=False,
            error="Git extractor not available",
        )

    # Create git-specific config
    git_config = GitRepoConfig(
        shallow=input.shallow,
        depth=input.depth,
        branch=input.branch,
        tag=input.tag,
        commit=input.commit,
        include_submodules=input.submodules,
        max_total_files=input.max_files,
        max_file_size=input.max_file_size,
        include_binary_metadata=input.include_binary,
    )

    registry = _create_registry()
    extractor = GitExtractor(
        config=git_config,
        token=input.token,
        registry=registry,
    )
    writer = OutputWriter(config)

    try:
        result = await extractor.extract(input.repo)
        output_path = await writer.write(result)

        # Extract repo name
        repo_name = input.repo.rstrip("/").split("/")[-1].replace(".git", "")

        return CloneRepoResult(
            success=True,
            output_path=str(output_path),
            repo_name=repo_name,
            files_processed=result.metadata.get("file_count", 0) if result.metadata else 0,
            files_skipped=result.metadata.get("skipped_count", 0) if result.metadata else 0,
            image_count=result.image_count if result.has_images else 0,
        )

    except Exception as e:
        return CloneRepoResult(
            success=False,
            error=str(e),
        )


@mcp.tool()
async def describe_images(input: DescribeImagesInput) -> DescribeImagesResult:
    """Generate VLM descriptions for images.

    Uses Ollama with a vision-language model to generate
    semantic descriptions of images. Useful for accessibility
    and RAG applications.

    Args:
        input: Description configuration

    Returns:
        Result with image descriptions

    Example:
        describe_images(input_path="./figure.png")
        describe_images(input_path="./images/", vlm_model="llava:13b")
    """
    try:
        from ingestor.ai.ollama.vlm import VLMDescriber
    except ImportError:
        return DescribeImagesResult(
            success=False,
            error="VLM dependencies not installed. Install with: uv sync --extra vlm",
        )

    input_path = Path(input.input_path)
    if not input_path.exists():
        return DescribeImagesResult(
            success=False,
            error=f"Path not found: {input.input_path}",
        )

    # Gather images
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
    if input_path.is_file():
        images = [input_path] if input_path.suffix.lower() in image_extensions else []
    else:
        images = [p for p in input_path.glob("**/*") if p.suffix.lower() in image_extensions]

    if not images:
        return DescribeImagesResult(
            success=False,
            error=f"No images found in {input.input_path}",
        )

    describer = VLMDescriber(host=input.ollama_host, model=input.vlm_model)
    descriptions = []

    for img_path in images:
        try:
            description = await describer.describe_file(img_path)
            descriptions.append({
                "file": str(img_path),
                "filename": img_path.name,
                "description": description,
            })
        except Exception as e:
            descriptions.append({
                "file": str(img_path),
                "filename": img_path.name,
                "error": str(e),
            })

    result = DescribeImagesResult(
        success=True,
        images_processed=len(descriptions),
        descriptions=descriptions[:100],  # Limit for response size
    )

    # Optionally write to file
    if input.output_file:
        import json
        output_path = Path(input.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(descriptions, f, indent=2)
        result.output_file = str(output_path)

    return result


@mcp.tool()
async def transcribe_audio(input: AudioTranscribeInput) -> AudioTranscribeResult:
    """Transcribe audio to text using Whisper.

    Converts audio files to text transcripts using OpenAI's Whisper model.
    Supports multiple languages with auto-detection.

    Args:
        input: Transcription configuration

    Returns:
        Result with transcript path

    Example:
        transcribe_audio(input_path="./lecture.mp3")
        transcribe_audio(input_path="./audio.wav", whisper_model="large", language="en")
    """
    from ingestor.output.writer import OutputWriter
    from ingestor.types import IngestConfig, MediaType

    config = IngestConfig(
        output_dir=Path(input.output_dir),
        verbose=input.verbose,
        whisper_model=input.whisper_model,
    )

    registry = _create_registry()
    writer = OutputWriter(config)

    # Get audio extractor
    extractor = registry.get(MediaType.AUDIO)
    if extractor is None:
        return AudioTranscribeResult(
            success=False,
            error="Audio extractor not available. Install with: uv sync --extra audio",
        )

    input_path = Path(input.input_path)
    if not input_path.exists():
        return AudioTranscribeResult(
            success=False,
            error=f"File not found: {input.input_path}",
        )

    try:
        result = await extractor.extract(str(input_path), config)
        output_path = await writer.write(result)

        return AudioTranscribeResult(
            success=True,
            output_path=str(output_path),
            duration=result.metadata.get("duration") if result.metadata else None,
            language=result.metadata.get("language") if result.metadata else None,
        )

    except Exception as e:
        return AudioTranscribeResult(
            success=False,
            error=str(e),
        )


# =============================================================================
# Helper Functions
# =============================================================================


def _create_registry():
    """Create extractor registry with available extractors."""
    from ingestor.core.registry import create_default_registry

    return create_default_registry()


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
