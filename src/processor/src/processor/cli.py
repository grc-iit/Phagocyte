"""Command-line interface for processor."""

import asyncio
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import load_config

console = Console()


@click.group()
@click.version_option(version=__version__)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """Processor - RAG chunking, embedding, and LanceDB loading."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@main.command()
@click.option("--skip-download", is_flag=True, help="Skip download, just check status")
@click.option("--minimal", is_flag=True, help="Only download qwen3-embedding:0.6b (minimal setup)")
@click.pass_context
def setup(ctx: click.Context, skip_download: bool, minimal: bool) -> None:
    """Download required embedding models via Ollama.

    \b
    Downloads embedding models for text and code:
      - qwen3-embedding:0.6b (text, 1024d) - compact, fast
      - jina-code-embeddings-0.5b (code, 896d) - code-specific

    \b
    Use --minimal for quick setup with just qwen3-embedding:0.6b.

    \b
    Prerequisites:
      - Ollama must be installed: https://ollama.com
      - Ollama server must be running: ollama serve
    """
    from .embedders.ollama import OllamaEmbedder

    # All models needed for full quality
    # Format: (profile, display_name, ollama_model)
    all_models = [
        ("text-low", "Qwen3-Embedding-0.6B", "qwen3-embedding:0.6b"),
        ("code-low", "jina-code-embeddings-0.5b", "hf.co/jinaai/jina-code-embeddings-0.5b-GGUF:Q8_0"),
        ("code-high", "jina-code-embeddings-1.5b", "hf.co/jinaai/jina-code-embeddings-1.5b-GGUF:Q8_0"),
    ]

    # Minimal setup: just qwen3-embedding
    minimal_models = [
        ("text/code", "Qwen3-Embedding-0.6B", "qwen3-embedding:0.6b"),
    ]

    models = minimal_models if minimal else all_models

    # Check if ollama CLI is available
    if not OllamaEmbedder.is_cli_available():
        console.print("[red]Error: ollama CLI not found![/red]")
        console.print("Please install Ollama from: https://ollama.com")
        console.print("Then ensure the server is running: ollama serve")
        return

    console.print("[bold]Ollama Embedding Model Setup[/bold]")
    if minimal:
        console.print("[dim](minimal mode - only downloading qwen3-embedding:0.6b)[/dim]")
    console.print()

    async def check_models() -> list[str]:
        embedder = OllamaEmbedder()
        return await embedder.list_models()

    # Check what's already available
    console.print("Checking available models...")
    try:
        import asyncio
        available = asyncio.run(check_models())
    except Exception:
        available = []

    for profile, name, ollama_model in models:
        is_available = any(ollama_model in m or m in ollama_model for m in available)
        status = "[green]Available[/green]" if is_available else "[yellow]Not found[/yellow]"
        console.print(f"  {profile}: {name} - {status}")

    if skip_download:
        console.print("\n[dim]--skip-download specified, not downloading.[/dim]")
        return

    console.print("\n[bold]Downloading models...[/bold]\n")

    downloaded_count = 0
    for profile, name, ollama_model in models:
        # Check if already available
        is_available = any(ollama_model in m or m in ollama_model for m in available)
        if is_available:
            console.print(f"  [dim]{profile}: {name} already available, skipping[/dim]")
            downloaded_count += 1
            continue

        console.print(f"  Downloading [cyan]{name}[/cyan] ({profile})...")
        console.print(f"    Model: {ollama_model}")
        success, output = OllamaEmbedder.pull_model(ollama_model)

        if success:
            console.print("    [green]Downloaded successfully[/green]")
            downloaded_count += 1
        else:
            console.print("    [red]Download failed[/red]")
            if output:
                console.print(f"    [dim]{output[:200]}[/dim]")

    console.print(f"\n[bold green]Setup complete![/bold green] ({downloaded_count}/{len(models)} models)")
    console.print("\nNext steps:")
    console.print("  1. Ensure Ollama is running: ollama serve")
    console.print("  2. Verify: uv run processor check")
    if not minimal:
        console.print("\nTip: Use --minimal for quick setup with just one model")


@main.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), default="./lancedb", help="LanceDB output path")
@click.option("--config", "config_path", type=click.Path(exists=True), help="Config YAML file")
@click.option(
    "--embedder",
    type=click.Choice(["ollama", "transformers"]),
    default="ollama",
    help="Embedding backend: ollama (default), transformers",
)
@click.option(
    "--text-profile",
    type=click.Choice(["low", "medium", "high"]),
    default="low",
    help="Text embedding profile",
)
@click.option(
    "--code-profile",
    type=click.Choice(["low", "high"]),
    default="low",
    help="Code embedding profile",
)
@click.option(
    "--multimodal-profile",
    type=click.Choice(["low", "high"]),
    default=None,
    help="Multimodal profile for unified table",
)
@click.option("--ollama-host", type=str, help="Ollama server URL")
@click.option("--torch-device", type=str, help="Torch device: auto, cuda, cpu")
@click.option(
    "--table-mode",
    type=click.Choice(["separate", "unified", "both"]),
    default="separate",
    help="DB table organization",
)
@click.option("--batch-size", type=int, default=32, help="Embedding batch size")
@click.option("--incremental/--full", default=True, help="Skip unchanged files")
@click.option(
    "--content-type",
    type=click.Choice(["auto", "code", "paper", "markdown"]),
    default="auto",
    help="Force content type",
)
@click.pass_context
def process(
    ctx: click.Context,
    input_path: str,
    output: str,
    config_path: str | None,
    embedder: str,
    text_profile: str,
    code_profile: str,
    multimodal_profile: str | None,
    ollama_host: str | None,
    torch_device: str | None,
    table_mode: str,
    batch_size: int,
    incremental: bool,
    content_type: str,
) -> None:
    """Process files through chunking, embedding, and loading.

    INPUT_PATH can be a file or directory.

    \b
    Backend options:
      --embedder ollama       Ollama with GGUF models (default)
      --embedder transformers HuggingFace models, requires GPU (torch)

    \b
    Ensure Ollama server is running before processing:
      ollama serve

    \b
    For multimodal/unified table (CLIP), use:
      --multimodal-profile low|high --table-mode unified
    """
    from .pipeline.processor import Pipeline

    async def run() -> None:
        # Load config
        config = load_config(Path(config_path) if config_path else None)

        # Merge CLI overrides
        config = config.merge_cli_args(
            output=output,
            embedder=embedder,
            text_profile=text_profile,
            code_profile=code_profile,
            multimodal_profile=multimodal_profile,
            ollama_host=ollama_host,
            torch_device=torch_device,
            table_mode=table_mode,
            batch_size=batch_size,
            incremental=incremental,
            verbose=ctx.obj.get("verbose", False),
        )

        console.print(f"[bold]Processing: {input_path}[/bold]")
        console.print(f"  Output: {output}")
        console.print(f"  Backend: {embedder}")
        console.print(f"  Table mode: {table_mode}")
        console.print(f"  Incremental: {incremental}")
        console.print()

        pipeline = Pipeline(config)
        result = await pipeline.process(Path(input_path), content_type=content_type)

        console.print("\n[bold green]Processing complete![/bold green]")
        console.print(f"  Files processed: {result.get('files_processed', 0)}")
        console.print(f"  Chunks created: {result.get('chunks_created', 0)}")
        console.print(f"  Images processed: {result.get('images_processed', 0)}")
        console.print(f"  Errors: {result.get('errors', 0)}")

    asyncio.run(run())


@main.command()
@click.option("--ollama-host", type=str, default="http://localhost:11434")
def check(ollama_host: str) -> None:
    """Check embedding service availability and models."""
    from .embedders.ollama import OllamaEmbedder

    async def run() -> None:
        console.print("[bold]Checking embedding backends...[/bold]\n")

        # Check Ollama CLI
        if OllamaEmbedder.is_cli_available():
            console.print("[green][OK] Ollama CLI[/green]")
            # Try to list models
            try:
                import subprocess
                result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout.strip():
                    console.print(f"  Available models:\n{result.stdout}")
            except Exception:
                pass
        else:
            console.print("[red][X] Ollama CLI[/red]: Not found")
            console.print("  Install from: https://ollama.com")

        console.print()

        # Check Ollama Server
        try:
            ollama = OllamaEmbedder(host=ollama_host)
            available = await ollama.is_available()
            if available:
                models = await ollama.list_models()
                console.print(f"[green][OK] Ollama Server[/green] ({ollama_host})")
                if models:
                    console.print(f"  Available models: {', '.join(models[:5])}")
                    if len(models) > 5:
                        console.print(f"  ... and {len(models) - 5} more")
                else:
                    console.print("  [yellow]No models - run: ollama pull qwen3-embedding:0.6b[/yellow]")
            else:
                console.print(f"[red][X] Ollama Server[/red] ({ollama_host}): Not available")
                console.print("  Start server with: ollama serve")
            await ollama.close()
        except Exception as e:
            console.print(f"[red][X] Ollama Server[/red] ({ollama_host}): Error - {e}")

        console.print()

        # Check Transformers/sentence-transformers
        try:
            import sentence_transformers
            import torch
            cuda_available = torch.cuda.is_available()
            cuda_info = ""
            if cuda_available:
                cuda_info = f", CUDA: {torch.cuda.get_device_name(0)}"
            console.print(f"[green][OK] Transformers[/green] (sentence-transformers {sentence_transformers.__version__}{cuda_info})")
            console.print("  Supports: jina-code-embeddings, Qwen3-Embedding via HuggingFace")
        except ImportError:
            console.print("[yellow][-] Transformers[/yellow]: Not installed")
            console.print("  Install with: uv sync --extra transformers")

        console.print()

        # Check OpenCLIP for multimodal
        try:
            import open_clip
            console.print(f"[green][OK] OpenCLIP[/green] (v{open_clip.__version__})")
            console.print("  Supports: CLIP, SigLIP for multimodal embeddings")
        except ImportError:
            console.print("[yellow][-] OpenCLIP[/yellow]: Not installed")
            console.print("  Install with: uv sync --extra multimodal")

        console.print()

        # Summary table
        from .embedders.profiles import EmbeddingProfiles

        table = Table(title="Model Availability by Backend")
        table.add_column("Domain", style="cyan")
        table.add_column("Profile", style="cyan")
        table.add_column("Model")
        table.add_column("Ollama")
        table.add_column("Transformers")

        for name, profile in EmbeddingProfiles.TEXT_PROFILES.items():
            table.add_row(
                "Text",
                name,
                profile.name,
                "[green]Yes[/green]" if profile.ollama_model else "[red]No[/red]",
                "[green]Yes[/green]" if profile.huggingface_id else "[red]No[/red]",
            )

        for name, profile in EmbeddingProfiles.CODE_PROFILES.items():
            table.add_row(
                "Code",
                name,
                profile.name,
                "[green]Yes[/green]" if profile.ollama_model else "[red]No[/red]",
                "[green]Yes[/green]" if profile.huggingface_id else "[red]No[/red]",
            )

        for name, profile in EmbeddingProfiles.MULTIMODAL_PROFILES.items():
            table.add_row(
                "Multimodal",
                name,
                profile.name,
                "[red]No[/red]",  # Multimodal requires transformers
                "[green]Yes[/green]" if profile.open_clip_model else "[red]No[/red]",
            )

        console.print(table)

    asyncio.run(run())


@main.command()
@click.argument("db_path", type=click.Path(exists=True))
@click.option("--table", type=str, help="Specific table to show stats for")
def stats(db_path: str, table: str | None) -> None:
    """Show database statistics."""
    import lancedb

    db = lancedb.connect(db_path)
    tables = db.table_names()

    console.print(f"[bold]Database: {db_path}[/bold]\n")
    console.print(f"Tables: {len(tables)}")

    stats_table = Table(title="Table Statistics")
    stats_table.add_column("Table", style="cyan")
    stats_table.add_column("Rows", justify="right")
    stats_table.add_column("Schema", style="dim")

    for tbl_name in tables:
        if table and tbl_name != table:
            continue
        tbl = db.open_table(tbl_name)
        row_count = tbl.count_rows()
        schema_cols = [f.name for f in tbl.schema][:4]
        schema_str = ", ".join(schema_cols)
        if len(tbl.schema) > 4:
            schema_str += f", ... (+{len(tbl.schema) - 4})"
        stats_table.add_row(tbl_name, str(row_count), schema_str)

    console.print(stats_table)


@main.command()
@click.argument("db_path", type=click.Path(exists=True))
@click.option("-o", "--output", required=True, type=click.Path(), help="Output directory")
@click.option(
    "--format",
    "export_format",
    type=click.Choice(["lance", "csv"]),
    default="lance",
    help="Export format",
)
@click.option("--bundle-config", is_flag=True, help="Include processor config")
@click.option("--tables", multiple=True, help="Specific tables to export")
@click.option("--include-vectors", is_flag=True, help="Include vectors in CSV (large!)")
def export(
    db_path: str,
    output: str,
    export_format: str,
    bundle_config: bool,
    tables: tuple[str, ...],
    include_vectors: bool,
) -> None:
    """Export database to portable format.

    \b
    Examples:
      processor export ./lancedb -o ./export --format lance
      processor export ./lancedb -o ./export --format csv
      processor export ./lancedb -o ./export --bundle-config
    """
    from .database.exporter import DatabaseExporter

    output_path = Path(output)
    exporter = DatabaseExporter(db_path)

    console.print(f"[bold]Exporting database: {db_path}[/bold]")
    console.print(f"  Format: {export_format}")
    console.print(f"  Output: {output}")

    # Get table list
    available_tables = exporter.list_tables()
    export_tables = list(tables) if tables else None

    if export_tables:
        # Validate requested tables exist
        missing = set(export_tables) - set(available_tables)
        if missing:
            console.print(f"[red]Tables not found: {', '.join(missing)}[/red]")
            console.print(f"Available: {', '.join(available_tables)}")
            return
        console.print(f"  Tables: {', '.join(export_tables)}")
    else:
        console.print(f"  Tables: {', '.join(available_tables)} (all)")

    console.print()

    # Export based on format
    if export_format == "lance":
        result = exporter.export_to_lance(output_path, export_tables)
    else:
        result = exporter.export_to_csv(output_path, export_tables, include_vectors)
        if not include_vectors:
            console.print("[dim]Note: Vector columns excluded from CSV (use --include-vectors to include)[/dim]")

    # Bundle config if requested
    config_path = None
    if bundle_config:
        config_path = exporter.bundle_config(output_path)
        if config_path:
            console.print(f"[green]Bundled config:[/green] {config_path.name}")
        else:
            console.print("[yellow]No config file found to bundle[/yellow]")

    # Write manifest
    manifest_path = exporter.export_manifest(output_path, export_format, result, config_path)

    # Summary
    console.print("\n[bold green]Export complete![/bold green]")
    console.print(f"  Location: {output_path}")
    console.print(f"  Manifest: {manifest_path.name}")

    stats_table = Table(title="Exported Tables")
    stats_table.add_column("Table", style="cyan")
    stats_table.add_column("Rows", justify="right")

    for table_name, row_count in result.items():
        stats_table.add_row(table_name, str(row_count))

    stats_table.add_row("[bold]Total[/bold]", f"[bold]{sum(result.values())}[/bold]")
    console.print(stats_table)


@main.command(name="import")
@click.argument("export_path", type=click.Path(exists=True))
@click.option("-o", "--output", required=True, type=click.Path(), help="Target database path")
@click.option("--tables", multiple=True, help="Specific tables to import")
def import_db(export_path: str, output: str, tables: tuple[str, ...]) -> None:
    """Import database from exported Lance format.

    \b
    Examples:
      processor import ./export -o ./lancedb_new
      processor import ./export -o ./lancedb_new --tables text_chunks code_chunks
    """
    from .database.exporter import DatabaseImporter

    importer = DatabaseImporter(output)
    export_dir = Path(export_path)

    console.print(f"[bold]Importing from: {export_path}[/bold]")
    console.print(f"  Target: {output}")

    # Check for manifest
    manifest = importer.read_manifest(export_dir)
    if manifest:
        console.print(f"  Source: {manifest.get('source_database', 'unknown')}")
        console.print(f"  Exported: {manifest.get('export_time', 'unknown')}")
        console.print(f"  Format: {manifest.get('format', 'unknown')}")
    else:
        console.print("[yellow]No manifest found - importing all Lance tables[/yellow]")

    console.print()

    import_tables = list(tables) if tables else None
    result = importer.import_from_lance(export_dir, import_tables)

    console.print("\n[bold green]Import complete![/bold green]")

    stats_table = Table(title="Imported Tables")
    stats_table.add_column("Table", style="cyan")
    stats_table.add_column("Rows", justify="right")

    for table_name, row_count in result.items():
        stats_table.add_row(table_name, str(row_count))

    stats_table.add_row("[bold]Total[/bold]", f"[bold]{sum(result.values())}[/bold]")
    console.print(stats_table)


@main.command()
@click.argument("db_path", type=click.Path(exists=True))
@click.option("--port", type=int, default=8000, help="Port for web viewer")
@click.option("--host", type=str, default="127.0.0.1", help="Host to bind")
def deploy(db_path: str, port: int, host: str) -> None:
    """Start a simple web interface to browse the database.

    \b
    Starts a local web server for browsing tables and running searches.

    \b
    Examples:
      processor deploy ./lancedb
      processor deploy ./lancedb --port 8080
    """
    import lancedb

    # Verify database exists and has tables
    db = lancedb.connect(db_path)
    tables = db.table_names()

    if not tables:
        console.print(f"[red]No tables found in {db_path}[/red]")
        return

    console.print(f"[bold]Database: {db_path}[/bold]")
    console.print(f"Tables: {', '.join(tables)}")
    console.print()

    # Try to use lancedb's built-in viewer if available
    try:
        # LanceDB Cloud has a viewer, but local doesn't have a built-in one
        # Check for common alternatives
        console.print("[bold]Starting database viewer...[/bold]")
        console.print()

        # Simple option: use datasette if available
        try:
            import subprocess

            # Check if datasette is available (works with Lance via plugin)
            result = subprocess.run(
                ["datasette", "--version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                console.print("[green]Datasette found![/green]")
                console.print("Note: For LanceDB, consider exporting to CSV first:")
                console.print(f"  processor export {db_path} -o ./export --format csv")
                console.print("  datasette ./export/*.csv")
                console.print()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # Provide guidance on viewing options
        console.print("[bold cyan]Database Viewing Options:[/bold cyan]")
        console.print()
        console.print("1. [bold]Command Line Search[/bold]")
        console.print(f"   processor search {db_path} \"your query\"")
        console.print()
        console.print("2. [bold]Python Interactive[/bold]")
        console.print("   import lancedb")
        console.print(f'   db = lancedb.connect("{db_path}")')
        console.print('   tbl = db.open_table("text_chunks")')
        console.print("   tbl.to_pandas().head()")
        console.print()
        console.print("3. [bold]Export to CSV[/bold] (view in Excel/spreadsheet)")
        console.print(f"   processor export {db_path} -o ./export --format csv")
        console.print()
        console.print("4. [bold]Jupyter Notebook[/bold]")
        console.print("   Great for interactive exploration with pandas")
        console.print()

        # Show quick stats
        console.print("[bold]Quick Stats:[/bold]")
        stats_table = Table()
        stats_table.add_column("Table", style="cyan")
        stats_table.add_column("Rows", justify="right")

        total = 0
        for tbl_name in tables:
            tbl = db.open_table(tbl_name)
            count = tbl.count_rows()
            total += count
            stats_table.add_row(tbl_name, str(count))

        stats_table.add_row("[bold]Total[/bold]", f"[bold]{total}[/bold]")
        console.print(stats_table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@main.command()
@click.argument("db_path", type=click.Path(exists=True))
@click.argument("query", type=str)
@click.option("--table", type=str, default="text_chunks", help="Table to search")
@click.option("-k", "--limit", type=int, default=5, help="Number of results")
@click.option("--hybrid", is_flag=True, help="Use hybrid search (vector + BM25)")
@click.option("--text-profile", type=click.Choice(["low", "medium", "high"]), help="Text embedding profile (overrides config)")
@click.option("--code-profile", type=click.Choice(["low", "high"]), help="Code embedding profile (overrides config)")
def search(db_path: str, query: str, table: str, limit: int, hybrid: bool, text_profile: str | None, code_profile: str | None) -> None:
    """Test search against the database."""
    from .embedders.ollama import OllamaEmbedder
    from .embedders.profiles import EmbeddingProfiles

    async def run() -> None:
        import lancedb

        # Get query embedding with correct model based on table
        config = load_config()

        # Select embedder based on table type
        if table == "code_chunks":
            profile_name = code_profile or config.embedding.code_profile
            profile = EmbeddingProfiles.get_code_profile(profile_name)
            model_name = profile.ollama_model or "jina-code-embeddings"
        else:
            profile_name = text_profile or config.embedding.text_profile
            profile = EmbeddingProfiles.get_text_profile(profile_name)
            model_name = profile.ollama_model or "qwen3-embedding:0.6b"

        embedder = OllamaEmbedder(model=model_name, host=config.embedding.ollama_host)

        console.print(f"[bold]Searching: {query}[/bold]\n")
        console.print(f"Using model: {model_name}")
        console.print("Generating query embedding...")

        try:
            query_embedding = await embedder.embed(query)
        except Exception as e:
            console.print(f"[red]Failed to generate embedding: {e}[/red]")
            return

        # Search database
        db = lancedb.connect(db_path)

        if table not in db.table_names():
            console.print(f"[red]Table '{table}' not found[/red]")
            console.print(f"Available tables: {', '.join(db.table_names())}")
            return

        tbl = db.open_table(table)

        if hybrid:
            console.print("Using hybrid search (vector + FTS)...")
            results = (
                tbl.search(query_type="hybrid")
                .vector(query_embedding)
                .text(query)
                .limit(limit)
                .to_list()
            )
        else:
            console.print("Using vector search...")
            results = tbl.search(query_embedding).limit(limit).to_list()

        console.print(f"\n[bold]Results ({len(results)}):[/bold]\n")

        for i, r in enumerate(results, 1):
            score = r.get("_distance", r.get("score", "N/A"))
            if isinstance(score, float):
                score = f"{score:.4f}"

            console.print(f"[bold cyan]Result {i}[/bold cyan] (distance: {score})")
            console.print(f"  Source: {r.get('source_file', 'unknown')}")

            content = r.get("content", "")
            if len(content) > 200:
                content = content[:200] + "..."
            console.print(f"  Content: {content}")
            console.print()

    asyncio.run(run())


@main.command(name="test-e2e")
@click.option(
    "--input",
    "input_path",
    type=click.Path(),
    default=None,
    help="Input directory for test data",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="lancedb_test",
    help="Test database output path",
)
@click.option("--cleanup", is_flag=True, help="Remove test database after validation")
@click.option("--skip-process", is_flag=True, help="Skip processing, just validate existing db")
@click.pass_context
def test_e2e(
    ctx: click.Context,
    input_path: str | None,
    output: str,
    cleanup: bool,
    skip_process: bool,
) -> None:
    """Run end-to-end validation test.

    \b
    Processes sample data, validates output, and runs test searches.

    \b
    Examples:
      processor test-e2e                           # Use input_reduced/
      processor test-e2e --input ./my_test_data
      processor test-e2e --cleanup                 # Remove db after test
    """
    import shutil

    import lancedb

    from .pipeline.processor import Pipeline

    async def run() -> None:
        # Find input_reduced directory (check tests/fixtures first, then root)
        if input_path:
            input_dir = Path(input_path)
        else:
            # Check standard locations
            fixtures_path = Path("tests/fixtures/input_reduced")
            root_path = Path("input_reduced")
            if fixtures_path.exists():
                input_dir = fixtures_path
            elif root_path.exists():
                input_dir = root_path
            else:
                input_dir = root_path  # Will fail with clear error message

        output_dir = Path(output)

        console.print("[bold]End-to-End Validation Test[/bold]")
        console.print(f"  Input: {input_dir}")
        console.print(f"  Output: {output_dir}")
        console.print()

        # Check input exists
        if not input_dir.exists():
            console.print(f"[red]Input directory not found: {input_dir}[/red]")
            console.print("Create test data with: processor test-e2e --input ./your_test_data")
            return

        errors = []
        warnings = []

        # Step 1: Process files
        if not skip_process:
            console.print("[bold cyan]Step 1: Processing files...[/bold cyan]")

            try:
                config = load_config()
                config = config.merge_cli_args(
                    output=output,
                    embedder="ollama",
                    text_profile="low",
                    code_profile="low",
                    table_mode="separate",
                    batch_size=32,
                    incremental=False,
                    verbose=ctx.obj.get("verbose", False),
                )

                pipeline = Pipeline(config)
                result = await pipeline.process(input_dir)

                console.print(f"  [green]Files processed: {result.get('files_processed', 0)}[/green]")
                console.print(f"  [green]Chunks created: {result.get('chunks_created', 0)}[/green]")
                console.print(f"  [green]Images processed: {result.get('images_processed', 0)}[/green]")

                if result.get("errors", 0) > 0:
                    errors.append(f"Processing had {result['errors']} errors")

            except Exception as e:
                console.print(f"  [red]Processing failed: {e}[/red]")
                errors.append(f"Processing failed: {e}")
                return

        else:
            console.print("[bold cyan]Step 1: Skipped (--skip-process)[/bold cyan]")

        # Step 2: Validate database
        console.print()
        console.print("[bold cyan]Step 2: Validating database...[/bold cyan]")

        if not output_dir.exists():
            console.print(f"  [red]Database not found: {output_dir}[/red]")
            errors.append("Database not created")
            return

        try:
            db = lancedb.connect(str(output_dir))
            tables = db.table_names()

            if not tables:
                errors.append("No tables created")
            else:
                console.print(f"  [green]Tables found: {', '.join(tables)}[/green]")

            # Check each expected table
            expected_tables = ["text_chunks", "code_chunks"]
            for expected in expected_tables:
                if expected in tables:
                    tbl = db.open_table(expected)
                    count = tbl.count_rows()
                    if count > 0:
                        console.print(f"  [green]{expected}: {count} rows[/green]")
                    else:
                        warnings.append(f"{expected} is empty")
                        console.print(f"  [yellow]{expected}: 0 rows[/yellow]")
                else:
                    warnings.append(f"{expected} table not found")
                    console.print(f"  [yellow]{expected}: not found[/yellow]")

            # Check for image_chunks if papers with figures exist
            if "image_chunks" in tables:
                tbl = db.open_table("image_chunks")
                count = tbl.count_rows()
                console.print(f"  [green]image_chunks: {count} rows[/green]")

        except Exception as e:
            console.print(f"  [red]Validation failed: {e}[/red]")
            errors.append(f"Validation failed: {e}")

        # Step 3: Test search (if embedder available)
        console.print()
        console.print("[bold cyan]Step 3: Testing search...[/bold cyan]")

        try:
            from .embedders.ollama import OllamaEmbedder

            config = load_config()
            embedder = OllamaEmbedder(host=config.embedding.ollama_host)

            if await embedder.is_available():
                test_queries = [
                    ("code_chunks", "function"),
                    ("text_chunks", "data"),
                ]

                for table_name, query in test_queries:
                    if table_name not in tables:
                        continue

                    try:
                        embedding = await embedder.embed(query)
                        tbl = db.open_table(table_name)
                        results = tbl.search(embedding).limit(3).to_list()
                        console.print(f"  [green]Search '{query}' in {table_name}: {len(results)} results[/green]")
                    except Exception as e:
                        warnings.append(f"Search test failed for {table_name}: {e}")
                        console.print(f"  [yellow]Search '{query}' failed: {e}[/yellow]")
                await embedder.close()
            else:
                console.print("  [yellow]Ollama not available - skipping search test[/yellow]")
                warnings.append("Search test skipped - Ollama not running")

        except Exception as e:
            console.print(f"  [yellow]Search test error: {e}[/yellow]")
            warnings.append(f"Search test error: {e}")

        # Summary
        console.print()
        console.print("[bold]Test Summary[/bold]")

        if errors:
            console.print(f"  [red]Errors: {len(errors)}[/red]")
            for err in errors:
                console.print(f"    - {err}")
        else:
            console.print("  [green]Errors: 0[/green]")

        if warnings:
            console.print(f"  [yellow]Warnings: {len(warnings)}[/yellow]")
            for warn in warnings:
                console.print(f"    - {warn}")
        else:
            console.print("  [green]Warnings: 0[/green]")

        # Cleanup if requested
        if cleanup and output_dir.exists():
            console.print()
            console.print("[dim]Cleaning up test database...[/dim]")
            shutil.rmtree(output_dir)
            console.print(f"  Removed: {output_dir}")

        # Final status
        console.print()
        if not errors:
            console.print("[bold green]✓ End-to-end test PASSED[/bold green]")
        else:
            console.print("[bold red]✗ End-to-end test FAILED[/bold red]")

    asyncio.run(run())


@main.command()
@click.argument("db_path", type=click.Path(exists=True))
@click.option("-p", "--port", type=int, default=8080, help="Port to serve on")
@click.option("--pull", is_flag=True, help="Pull the Docker image first")
def visualize(db_path: str, port: int, pull: bool) -> None:
    """Launch lance-data-viewer to browse the database.

    Requires Docker to be installed and running.

    \b
    Examples:
      processor visualize ./lancedb
      processor visualize ./lancedb -p 9000
      processor visualize ./lancedb --pull

    Access the viewer at http://localhost:PORT after launch.
    """
    import os
    import subprocess

    db_path = os.path.abspath(db_path)
    image = "ghcr.io/gordonmurray/lance-data-viewer:lancedb-0.24.3"

    console.print("[bold]Lance Data Viewer[/bold]")
    console.print(f"  Database: {db_path}")
    console.print(f"  Port: {port}")
    console.print(f"  Image: {image}")
    console.print()

    # Pull image if requested
    if pull:
        console.print("Pulling Docker image...")
        result = subprocess.run(["docker", "pull", image], capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[red]Failed to pull image: {result.stderr}[/red]")
            return
        console.print("[green]Image pulled successfully[/green]")
        console.print()

    # Check if Docker is available
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            console.print("[red]Docker is not available. Please install Docker.[/red]")
            return
    except FileNotFoundError:
        console.print("[red]Docker command not found. Please install Docker.[/red]")
        return

    console.print(f"Launching viewer at [bold cyan]http://localhost:{port}[/bold cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")
    console.print()

    # Run the container
    # On Windows, convert path for Docker volume mount
    if os.name == "nt":
        # Convert Windows path to Docker-compatible format
        db_path = db_path.replace("\\", "/")
        # For Docker on Windows, we may need //host format
        if db_path[1] == ":":
            db_path = "/" + db_path[0].lower() + db_path[2:]

    cmd = [
        "docker", "run", "--rm",
        "-p", f"{port}:8080",
        "-v", f"{db_path}:/data:ro",
        image
    ]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n[yellow]Viewer stopped[/yellow]")


@main.command()
@click.argument("db_path", type=click.Path(exists=True))
@click.option("-p", "--port", type=int, default=8000, help="Port for REST API server")
@click.option("--build", is_flag=True, help="Build the Docker image first")
@click.option("--detach", "-d", is_flag=True, help="Run in background (detached mode)")
def server(db_path: str, port: int, build: bool, detach: bool) -> None:
    """Deploy LanceDB as a REST API server via Docker.

    Starts a FastAPI server that wraps the LanceDB database,
    exposing search endpoints for remote access.

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
    Example:
      processor server ./lancedb --port 8000
      curl http://localhost:8000/tables
    """
    import os
    import subprocess

    db_path = os.path.abspath(db_path)
    image = "processor-lancedb-server:latest"

    console.print("\n[bold]LanceDB REST API Server[/bold]")
    console.print(f"  Database: {db_path}")
    console.print(f"  Port: {port}")
    console.print(f"  Image: {image}")
    console.print()

    # Check Docker is available
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            console.print("[red]Docker not available[/red]")
            return
    except FileNotFoundError:
        console.print("[red]Docker command not found. Please install Docker.[/red]")
        return

    # Build image if requested or if it doesn't exist
    if build:
        console.print("Building Docker image...")

        # Find Dockerfile
        import processor
        pkg_dir = Path(processor.__file__).parent.parent.parent
        dockerfile_dir = pkg_dir / "docker" / "lancedb-server"

        if not dockerfile_dir.exists():
            console.print(f"[red]Dockerfile not found at {dockerfile_dir}[/red]")
            return

        result = subprocess.run(
            ["docker", "build", "-t", image, str(dockerfile_dir)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            console.print(f"[red]Build failed: {result.stderr}[/red]")
            return

        console.print("[green]Image built successfully[/green]")
        console.print()

    # Check if image exists
    result = subprocess.run(
        ["docker", "images", "-q", image],
        capture_output=True,
        text=True,
    )
    if not result.stdout.strip():
        console.print(f"[yellow]Image '{image}' not found. Building...[/yellow]")

        import processor
        pkg_dir = Path(processor.__file__).parent.parent.parent
        dockerfile_dir = pkg_dir / "docker" / "lancedb-server"

        if not dockerfile_dir.exists():
            console.print(f"[red]Dockerfile not found at {dockerfile_dir}[/red]")
            console.print("Run 'processor server --build' to build the image.")
            return

        result = subprocess.run(
            ["docker", "build", "-t", image, str(dockerfile_dir)],
            text=True,
        )

        if result.returncode != 0:
            console.print("[red]Build failed[/red]")
            return

        console.print("[green]Image built successfully[/green]")
        console.print()

    # Convert path for Docker on Windows
    if os.name == "nt":
        db_path = db_path.replace("\\", "/")
        if db_path[1] == ":":
            db_path = "/" + db_path[0].lower() + db_path[2:]

    cmd = [
        "docker", "run", "--rm",
        "-p", f"{port}:8000",
        "-v", f"{db_path}:/data:ro",
        "-e", "LANCEDB_PATH=/data",
        image
    ]

    if detach:
        cmd.insert(2, "-d")
        cmd.insert(3, "--name")
        cmd.insert(4, "lancedb-server")

    console.print(f"Starting server at [bold cyan]http://localhost:{port}[/bold cyan]")

    if detach:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            container_id = result.stdout.strip()[:12]
            console.print(f"[green]Server running in background (container: {container_id})[/green]")
            console.print()
            console.print("[dim]Stop with: docker stop lancedb-server[/dim]")
        else:
            console.print(f"[red]Failed to start: {result.stderr}[/red]")
    else:
        console.print("[dim]Press Ctrl+C to stop[/dim]")
        console.print()
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            console.print("\n[yellow]Server stopped[/yellow]")


if __name__ == "__main__":
    main()
