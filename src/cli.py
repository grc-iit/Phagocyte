"""Phagocyte CLI - Unified interface for the research pipeline.

Structure:
  phagocyte research <cmd>  - AI-powered deep research
  phagocyte parse <cmd>     - Reference parsing & paper acquisition
  phagocyte ingest <cmd>    - Document/media to markdown
  phagocyte process <cmd>   - Chunking, embedding, vector store
"""

import subprocess
import sys
from pathlib import Path

import click


def get_src() -> Path:
    """Get the src directory."""
    return Path(__file__).parent


def run_module(module: str, args: list[str]) -> int:
    """Run a command in a module directory."""
    cwd = get_src() / module
    cmd = ["uv", "run", module] + args
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode


# =============================================================================
# Main CLI
# =============================================================================


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Phagocyte - End-to-end research pipeline.

    \b
    Pipeline: Research → Parse → Ingest → Process → Search

    \b
    Commands:
      research  - AI-powered deep research (Gemini)
      parse     - Reference extraction & paper acquisition
      ingest    - Document/media to markdown conversion
      process   - Chunking, embedding, LanceDB vector store
    """
    pass


# =============================================================================
# RESEARCH Command (direct command, not a group)
# =============================================================================


@cli.command()
@click.argument("topic")
@click.option("-o", "--output", help="Output directory")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(["undirected", "directed", "no-research"]),
    default="undirected",
    help="Research mode",
)
@click.option(
    "-a",
    "--artifact",
    "artifacts",
    multiple=True,
    help="Artifact URLs (can specify multiple)",
)
@click.option("--api-key", help="Gemini API key")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def research(topic, output, mode, artifacts, api_key, verbose):
    """AI-powered deep research using Gemini.

    \b
    Modes:
      undirected  - Web-first discovery (default)
      directed    - Use artifacts first, fill gaps with web
      no-research - Analyze only provided artifacts

    \b
    Examples:
      phagocyte research "HDF5 best practices"
      phagocyte research "RAG systems" -m directed -a "https://docs.example.com"
    """
    args = ["research", topic, "--mode", mode]
    if output:
        args.extend(["-o", output])
    for a in artifacts:
        args.extend(["-a", a])
    if api_key:
        args.extend(["--api-key", api_key])
    if verbose:
        args.append("-v")
    sys.exit(run_module("researcher", args))


# =============================================================================
# PARSE Command Group (10 commands)
# =============================================================================


@cli.group()
def parse():
    """Reference extraction & paper acquisition.

    \b
    Commands:
      refs      - Parse references from a document
      retrieve  - Download a single paper
      batch     - Batch download papers
      doi2bib   - Convert DOI to BibTeX
      verify    - Verify citations against CrossRef
      citations - Get citation graph
      sources   - List available paper sources
      auth      - Authenticate with institution
      init      - Initialize configuration
      config    - Manage config sync (push/pull)
    """
    pass


@parse.command("refs")
@click.argument("input_file")
@click.option("-o", "--output", help="Output directory")
@click.option(
    "--agent",
    type=click.Choice(["none", "claude", "gemini"]),
    default="none",
    help="AI agent for parsing",
)
@click.option("--export-batch", is_flag=True, help="Export batch.json for acquisition")
@click.option("--export-dois", is_flag=True, help="Export dois.txt for doi2bib")
@click.option("--compare", is_flag=True, help="Compare regex vs agent parsing")
def parse_refs(input_file, output, agent, export_batch, export_dois, compare):
    """Parse references from a research document.

    \b
    Examples:
      phagocyte parse refs research_report.md --export-batch
      phagocyte parse refs paper.md --agent claude --compare
    """
    args = ["parse-refs", input_file]
    if output:
        args.extend(["-o", output])
    if agent != "none":
        args.extend(["--agent", agent])
    if export_batch:
        args.append("--export-batch")
    if export_dois:
        args.append("--export-dois")
    if compare:
        args.append("--compare")
    sys.exit(run_module("parser", args))


@parse.command("retrieve")
@click.argument("identifier")
@click.option("-o", "--output", default="./papers", help="Output directory")
@click.option("--email", envvar="PAPER_EMAIL", help="Email for API access")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def parse_retrieve(identifier, output, email, verbose):
    """Download a single paper by DOI, title, or arXiv ID.

    \b
    Examples:
      phagocyte parse retrieve "10.1038/nature12373"
      phagocyte parse retrieve "arXiv:2005.11401"
      phagocyte parse retrieve "Attention Is All You Need"
    """
    args = ["retrieve", identifier, "-o", output]
    if email:
        args.extend(["--email", email])
    if verbose:
        args.append("-v")
    sys.exit(run_module("parser", args))


@parse.command("batch")
@click.argument("input_file")
@click.option("-o", "--output", default="./papers", help="Output directory")
@click.option("-n", "--concurrent", default=3, help="Max concurrent downloads")
@click.option("--email", envvar="PAPER_EMAIL", help="Email for API access")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def parse_batch(input_file, output, concurrent, email, verbose):
    """Batch download papers from a file.

    \b
    Supports: JSON, CSV, TXT (one ID per line)

    \b
    Examples:
      phagocyte parse batch batch.json -o ./papers
      phagocyte parse batch dois.txt -n 5
    """
    args = ["batch", input_file, "-o", output, "-n", str(concurrent)]
    if email:
        args.extend(["--email", email])
    if verbose:
        args.append("-v")
    sys.exit(run_module("parser", args))


@parse.command("doi2bib")
@click.argument("identifier", required=False)
@click.option("-i", "--input", "input_file", help="File with DOIs")
@click.option("-o", "--output", help="Output file")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["bibtex", "json", "markdown"]),
    default="bibtex",
)
def parse_doi2bib(identifier, input_file, output, fmt):
    """Convert DOI or arXiv ID to BibTeX/JSON/Markdown.

    \b
    Examples:
      phagocyte parse doi2bib 10.1038/nature12373
      phagocyte parse doi2bib -i dois.txt -o references.bib
    """
    args = ["doi2bib"]
    if identifier:
        args.append(identifier)
    if input_file:
        args.extend(["-i", input_file])
    if output:
        args.extend(["-o", output])
    args.extend(["--format", fmt])
    sys.exit(run_module("parser", args))


@parse.command("verify")
@click.argument("input_path")
@click.option("-o", "--output", help="Output directory")
@click.option("--email", envvar="PAPER_EMAIL", help="Email for CrossRef")
@click.option("--dry-run", is_flag=True, help="Don't write files")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def parse_verify(input_path, output, email, dry_run, verbose):
    """Verify BibTeX citations against CrossRef and arXiv.

    \b
    Examples:
      phagocyte parse verify references.bib -o ./verified
      phagocyte parse verify citations_dir/ --dry-run
    """
    args = ["verify", input_path]
    if output:
        args.extend(["-o", output])
    if email:
        args.extend(["--email", email])
    if dry_run:
        args.append("--dry-run")
    if verbose:
        args.append("-v")
    sys.exit(run_module("parser", args))


@parse.command("citations")
@click.argument("identifier")
@click.option(
    "--direction",
    type=click.Choice(["citations", "references", "both"]),
    default="both",
)
@click.option("-n", "--limit", default=50, help="Max items to retrieve")
@click.option("-o", "--output", help="Output file")
@click.option(
    "--format", "fmt", type=click.Choice(["json", "text", "bibtex"]), default="text"
)
def parse_citations(identifier, direction, limit, output, fmt):
    """Get citation graph for a paper.

    \b
    Examples:
      phagocyte parse citations "10.1038/nature12373" --direction both
      phagocyte parse citations "arXiv:2005.11401" -n 100 --format bibtex
    """
    args = [
        "citations",
        identifier,
        "--direction",
        direction,
        "-n",
        str(limit),
        "--format",
        fmt,
    ]
    if output:
        args.extend(["-o", output])
    sys.exit(run_module("parser", args))


@parse.command("sources")
def parse_sources():
    """List available paper sources and their status."""
    sys.exit(run_module("parser", ["sources"]))


@parse.command("auth")
def parse_auth():
    """Authenticate with your institution for access to IEEE, ACM, etc.

    \b
    Two modes:
      1. VPN Mode: Configure vpn_enabled: true and vpn_script
      2. EZProxy Mode: Configure proxy_url, then run this command
    """
    sys.exit(run_module("parser", ["auth"]))


@parse.command("init")
def parse_init():
    """Initialize a configuration file.

    Creates a config.yaml file with default settings.
    """
    sys.exit(run_module("parser", ["init"]))


@parse.group("config")
def parse_config():
    """Manage configuration sync across machines."""
    pass


@parse_config.command("push")
def parse_config_push():
    """Push config to a private GitHub gist."""
    sys.exit(run_module("parser", ["config", "push"]))


@parse_config.command("pull")
def parse_config_pull():
    """Pull config from a private GitHub gist."""
    sys.exit(run_module("parser", ["config", "pull"]))


# =============================================================================
# INGEST Command Group (5 commands)
# =============================================================================


@cli.group()
def ingest():
    """Document/media to markdown conversion.

    \b
    Commands:
      file      - Ingest a single file or URL
      batch     - Process all files in a folder
      crawl     - Deep crawl a website
      clone     - Clone and ingest a git repo
      describe  - Generate VLM image descriptions
    """
    pass


@ingest.command("file")
@click.argument("source")
@click.option("-o", "--output", default="./output", help="Output directory")
@click.option("--describe-images", is_flag=True, help="Generate VLM image descriptions")
@click.option("--img-format", type=click.Choice(["png", "jpg", "webp"]), default="png")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def ingest_file(source, output, describe_images, img_format, verbose):
    """Ingest a single file or URL to markdown.

    \b
    Supports: PDF, DOCX, PPTX, EPUB, HTML, YouTube, etc.

    \b
    Examples:
      phagocyte ingest file paper.pdf -o ./output
      phagocyte ingest file https://youtube.com/watch?v=xxx
      phagocyte ingest file document.docx --describe-images
    """
    args = ["ingest", source, "-o", output, "--img-to", img_format]
    if describe_images:
        args.append("--describe")
    if verbose:
        args.append("-v")
    sys.exit(run_module("ingestor", args))


@ingest.command("batch")
@click.argument("input_dir")
@click.option("-o", "--output", default="./output", help="Output directory")
@click.option("--recursive/--no-recursive", default=True, help="Process subdirectories")
@click.option("-n", "--concurrency", default=5, help="Max concurrent extractions")
@click.option("--describe-images", is_flag=True, help="Generate VLM image descriptions")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def ingest_batch(input_dir, output, recursive, concurrency, describe_images, verbose):
    """Process all supported files in a folder.

    \b
    Examples:
      phagocyte ingest batch ./papers -o ./markdown
      phagocyte ingest batch ./docs --describe-images -n 10
    """
    args = ["batch", input_dir, "-o", output, "--concurrency", str(concurrency)]
    if not recursive:
        args.append("--no-recursive")
    if describe_images:
        args.append("--describe")
    if verbose:
        args.append("-v")
    sys.exit(run_module("ingestor", args))


@ingest.command("crawl")
@click.argument("url")
@click.option("-o", "--output", default="./output", help="Output directory")
@click.option("--max-pages", default=50, help="Maximum pages to crawl")
@click.option("--max-depth", default=2, help="Maximum crawl depth")
@click.option(
    "--strategy", type=click.Choice(["bfs", "dfs", "bestfirst"]), default="bfs"
)
@click.option("--include", multiple=True, help="URL patterns to include (can use multiple times)")
@click.option("--exclude", multiple=True, help="URL patterns to exclude (can use multiple times)")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def ingest_crawl(url, output, max_pages, max_depth, strategy, include, exclude, verbose):
    """Deep crawl a website and convert to markdown.

    \b
    Strategies:
      bfs       - Breadth-first (level by level)
      dfs       - Depth-first (follow links deep)
      bestfirst - Prioritize content-rich pages

    \b
    Examples:
      phagocyte ingest crawl https://docs.example.com -o ./docs
      phagocyte ingest crawl https://site.com --max-pages 100 --max-depth 3
    """
    args = [
        "crawl",
        url,
        "-o",
        output,
        "--max-pages",
        str(max_pages),
        "--max-depth",
        str(max_depth),
        "--strategy",
        strategy,
    ]
    for pattern in include:
        args.extend(["--include", pattern])
    for pattern in exclude:
        args.extend(["--exclude", pattern])
    if verbose:
        args.append("-v")
    sys.exit(run_module("ingestor", args))


@ingest.command("clone")
@click.argument("repo")
@click.option("-o", "--output", default="./output", help="Output directory")
@click.option("--branch", help="Clone specific branch")
@click.option("--token", envvar="GITHUB_TOKEN", help="Git token for private repos")
@click.option("--max-files", type=int, default=10000, help="Maximum files to process")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def ingest_clone(repo, output, branch, token, max_files, verbose):
    """Clone and ingest a git repository.

    \b
    Examples:
      phagocyte ingest clone https://github.com/user/repo
      phagocyte ingest clone https://github.com/user/repo --branch develop
      phagocyte ingest clone git@github.com:user/repo.git --token $TOKEN
    """
    args = ["clone", repo, "-o", output]
    if branch:
        args.extend(["--branch", branch])
    if token:
        args.extend(["--token", token])
    if max_files:
        args.extend(["--max-files", str(max_files)])
    if verbose:
        args.append("-v")
    sys.exit(run_module("ingestor", args))


@ingest.command("describe")
@click.argument("input_path")
@click.option("--model", default="llava:7b", help="VLM model")
@click.option("-o", "--output", help="Output JSON file")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def ingest_describe(input_path, model, output, verbose):
    """Generate VLM descriptions for images.

    \b
    Examples:
      phagocyte ingest describe ./images/
      phagocyte ingest describe figure.png --model llava:13b
    """
    args = ["describe", input_path, "--model", model]
    if output:
        args.extend(["-o", output])
    if verbose:
        args.append("-v")
    sys.exit(run_module("ingestor", args))


# =============================================================================
# PROCESS Command Group (11 commands)
# =============================================================================


@cli.group()
def process():
    """Chunking, embedding, and LanceDB vector store.

    \b
    Commands:
      run       - Process files into vector database
      search    - Search the vector database
      stats     - Show database statistics
      setup     - Download embedding models
      check     - Check service availability
      export    - Export database
      import    - Import database
      visualize - Browse database with viewer
      deploy    - Start web interface
      server    - Deploy LanceDB REST API server
      test-e2e  - Run end-to-end validation test
    """
    pass


@process.command("run")
@click.argument("input_path")
@click.option("-o", "--output", default="./lancedb", help="LanceDB output path")
@click.option(
    "--text-profile",
    type=click.Choice(["low", "medium", "high"]),
    default="low",
    help="Text embedding quality",
)
@click.option(
    "--code-profile",
    type=click.Choice(["low", "high"]),
    default="low",
    help="Code embedding quality",
)
@click.option(
    "--table-mode",
    type=click.Choice(["separate", "unified", "both"]),
    default="separate",
)
@click.option("--incremental", is_flag=True, help="Skip unchanged files")
@click.option("--full", is_flag=True, help="Process all files (disable incremental)")
@click.option("--batch-size", default=32, help="Embedding batch size")
@click.option("--chunk-only", is_flag=True, help="Only chunk files, skip embedding")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def process_run(
    input_path,
    output,
    text_profile,
    code_profile,
    table_mode,
    incremental,
    full,
    batch_size,
    chunk_only,
    verbose,
):
    """Process files through chunking, embedding, and loading into LanceDB.

    \b
    Examples:
      phagocyte process run ./markdown -o ./lancedb
      phagocyte process run ./code --text-profile medium --incremental
      phagocyte process run ./docs --chunk-only --full
    """
    args = [
        "process",
        input_path,
        "-o",
        output,
        "--text-profile",
        text_profile,
        "--code-profile",
        code_profile,
        "--table-mode",
        table_mode,
        "--batch-size",
        str(batch_size),
    ]
    if incremental:
        args.append("--incremental")
    elif full:
        args.append("--full")
    if chunk_only:
        args.append("--chunk-only")
    if verbose:
        args.append("-v")
    sys.exit(run_module("processor", args))


@process.command("search")
@click.argument("db_path")
@click.argument("query")
@click.option("-k", "--limit", default=5, help="Number of results")
@click.option(
    "--table",
    type=click.Choice(["text_chunks", "code_chunks", "chunks"]),
    default="text_chunks",
)
@click.option("--hybrid", is_flag=True, help="Use hybrid search (vector + BM25)")
@click.option("--rerank", is_flag=True, help="Rerank results with cross-encoder")
@click.option(
    "--text-profile",
    type=click.Choice(["low", "medium", "high"]),
    help="Text embedding profile (must match what was used during processing)",
)
@click.option(
    "--code-profile",
    type=click.Choice(["low", "high"]),
    help="Code embedding profile (must match what was used during processing)",
)
def process_search(db_path, query, limit, table, hybrid, rerank, text_profile, code_profile):
    """Search the vector database.

    \b
    Examples:
      phagocyte process search ./lancedb "chunking strategies"
      phagocyte process search ./lancedb "authentication" --table code_chunks --hybrid
    """
    args = ["search", db_path, query, "-k", str(limit), "--table", table]
    if hybrid:
        args.append("--hybrid")
    if rerank:
        args.append("--rerank")
    if text_profile:
        args.extend(["--text-profile", text_profile])
    if code_profile:
        args.extend(["--code-profile", code_profile])
    sys.exit(run_module("processor", args))


@process.command("stats")
@click.argument("db_path")
@click.option("--table", help="Specific table to inspect")
def process_stats(db_path, table):
    """Show database statistics.

    \b
    Examples:
      phagocyte process stats ./lancedb
      phagocyte process stats ./lancedb --table text_chunks
    """
    args = ["stats", db_path]
    if table:
        args.extend(["--table", table])
    sys.exit(run_module("processor", args))


@process.command("setup")
@click.option(
    "--minimal/--full", default=True, help="Download minimal or full model set"
)
def process_setup(minimal):
    """Download required embedding models via Ollama.

    \b
    Minimal: qwen3-embedding:0.6b (text only)
    Full: Also includes jina-code models
    """
    args = ["setup"]
    if minimal:
        args.append("--minimal")
    sys.exit(run_module("processor", args))


@process.command("check")
def process_check():
    """Check embedding service availability and models."""
    sys.exit(run_module("processor", ["check"]))


@process.command("export")
@click.argument("db_path")
@click.argument("output_path")
@click.option("--format", "fmt", type=click.Choice(["lance", "csv"]), default="lance")
@click.option("--include-vectors", is_flag=True, help="Include vectors in CSV export")
def process_export(db_path, output_path, fmt, include_vectors):
    """Export database to portable format.

    \b
    Examples:
      phagocyte process export ./lancedb ./backup
      phagocyte process export ./lancedb ./data.csv --format csv
    """
    args = ["export", db_path, output_path, "--format", fmt]
    if include_vectors:
        args.append("--include-vectors")
    sys.exit(run_module("processor", args))


@process.command("import")
@click.argument("export_path")
@click.argument("output_path")
def process_import(export_path, output_path):
    """Import database from exported Lance format.

    \b
    Examples:
      phagocyte process import ./backup ./lancedb
    """
    sys.exit(run_module("processor", ["import", export_path, output_path]))


@process.command("visualize")
@click.argument("db_path")
def process_visualize(db_path):
    """Launch lance-data-viewer to browse the database."""
    sys.exit(run_module("processor", ["visualize", db_path]))


@process.command("deploy")
@click.argument("db_path")
@click.option("--port", default=8000, help="Server port")
def process_deploy(db_path, port):
    """Start a simple web interface to browse the database."""
    sys.exit(run_module("processor", ["deploy", db_path, "--port", str(port)]))


@process.command("server")
@click.argument("db_path")
@click.option("-p", "--port", default=8000, help="Port for REST API server")
@click.option("--build", is_flag=True, help="Build the Docker image first")
@click.option("-d", "--detach", is_flag=True, help="Run in background (detached mode)")
def process_server(db_path, port, build, detach):
    """Deploy LanceDB as a REST API server via Docker.

    \b
    API Endpoints:
      GET  /tables                       - List all tables
      GET  /tables/{name}                - Table info
      GET  /tables/{name}/schema         - Table schema
      GET  /tables/{name}/rows           - Get rows (paginated)
      POST /tables/{name}/search         - Vector search
      POST /tables/{name}/search/hybrid  - Hybrid search (vector + FTS)
      POST /tables/{name}/search/text    - Full-text search
      GET  /metadata                     - Database metadata

    \b
    Examples:
      phagocyte process server ./lancedb --port 8000
      curl http://localhost:8000/tables
    """
    args = ["server", db_path, "-p", str(port)]
    if build:
        args.append("--build")
    if detach:
        args.append("-d")
    sys.exit(run_module("processor", args))


@process.command("test-e2e")
@click.option("--input", "input_path", help="Input directory for test data")
@click.option("-o", "--output", help="Test database output path")
@click.option("--cleanup", is_flag=True, help="Remove test database after validation")
@click.option(
    "--skip-process", is_flag=True, help="Skip processing, just validate existing db"
)
def process_test_e2e(input_path, output, cleanup, skip_process):
    """Run end-to-end validation test.

    \b
    Processes sample data, validates output, and runs test searches.

    \b
    Examples:
      phagocyte process test-e2e                      # Use input_reduced/
      phagocyte process test-e2e --input ./my_data
      phagocyte process test-e2e --cleanup            # Remove db after test
    """
    args = ["test-e2e"]
    if input_path:
        args.extend(["--input", input_path])
    if output:
        args.extend(["-o", output])
    if cleanup:
        args.append("--cleanup")
    if skip_process:
        args.append("--skip-process")
    sys.exit(run_module("processor", args))


def main():
    cli()


if __name__ == "__main__":
    main()
