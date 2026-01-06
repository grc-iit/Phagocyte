"""CLI for Parser module - Retrieve papers and parse references.

Commands from paper-acq:
- retrieve: Retrieve single paper with multi-source fallback
- batch: Batch download papers
- sources: List available sources and status
- init: Create config file
- auth: Institutional authentication
- config push/pull: Sync config via GitHub gist

Commands from doi2bib:
- doi2bib: Convert DOI/arXiv to BibTeX/JSON/Markdown
- verify: Verify BibTeX citations (single file or directory)

New commands:
- parse-refs: Extract references from research documents
- citations: Get citation graph for a paper
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

import click


@click.group()
@click.option(
    "-c", "--config",
    "config_path",
    default=None,
    help="Configuration file path",
    type=click.Path(),
)
@click.pass_context
def cli(ctx: click.Context, config_path: str | None) -> None:
    """Parser CLI - Retrieve papers, verify citations, and parse references."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path


# =============================================================================
# Commands from paper-acq
# =============================================================================

@cli.command("retrieve")
@click.argument("identifier", required=False)
@click.option("-d", "--doi", help="Paper DOI")
@click.option("-t", "--title", help="Paper title")
@click.option("-o", "--output", default=None, help="Output directory (uses config if not set)")
@click.option("-e", "--email", envvar="PAPER_EMAIL", help="Email for API access")
@click.option("--s2-key", envvar="S2_API_KEY", help="Semantic Scholar API key")
@click.option("--skip-existing/--no-skip-existing", default=None, help="Skip if PDF exists (uses config if not set)")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.pass_context
def retrieve_paper(
    ctx: click.Context,
    identifier: str | None,
    doi: str | None,
    title: str | None,
    output: str | None,
    email: str | None,
    s2_key: str | None,
    skip_existing: bool | None,
    verbose: bool,
):
    """Retrieve a single paper PDF.

    Tries sources in priority order: unpaywall, arxiv, pmc, semantic_scholar, etc.

    Examples:
        parser retrieve --doi "10.1038/nature12373"
        parser retrieve --title "Attention Is All You Need"
        parser retrieve -d "10.1038/nature12373" -o ./papers -e you@email.com
        parser retrieve "arXiv:2005.11401" -o ./papers
    """
    # Resolve identifier from positional arg or --doi/--title options
    if not identifier and not doi and not title:
        raise click.UsageError("Must provide IDENTIFIER, --doi, or --title")

    # At this point, at least one of identifier, doi, or title is not None
    final_identifier: str
    if identifier:
        final_identifier = identifier
    elif doi:
        final_identifier = doi
    elif title:
        final_identifier = title
    else:
        raise click.UsageError("Must provide IDENTIFIER, --doi, or --title")

    from .acquisition.config import Config
    from .acquisition.retriever import PaperRetriever, RetrievalStatus

    config = Config.load(ctx.obj.get("config_path"))
    if email:
        config.email = email
    if s2_key:
        config.api_keys["semantic_scholar"] = s2_key
    if skip_existing is not None:
        config.download["skip_existing"] = skip_existing

    # Use config output_dir as default
    output_dir = Path(output) if output else config.get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)

    retriever = PaperRetriever(config)

    # Parse identifier
    doi, title, pdf_url = _parse_identifier(final_identifier)

    # Handle direct PDF URL
    if pdf_url:
        if verbose:
            click.echo(f"Direct PDF URL: {pdf_url}")
            click.echo(f"Output: {output_dir}")

        # Download directly
        import httpx
        try:
            # Create filename from URL
            from urllib.parse import urlparse
            parsed = urlparse(pdf_url)
            filename = Path(parsed.path).name
            if not filename.endswith('.pdf'):
                filename = f"downloaded_{hash(pdf_url) % 10000}.pdf"

            output_path = output_dir / filename

            with httpx.Client(follow_redirects=True, timeout=60.0) as client:
                response = client.get(pdf_url)
                response.raise_for_status()
                output_path.write_bytes(response.content)

            click.echo(click.style("✓ Downloaded: ", fg="green") + str(output_path))
            click.echo("  Source: direct URL")
            return
        except Exception as e:
            click.echo(click.style("✗ Failed: ", fg="red") + str(e), err=True)
            sys.exit(1)

    if verbose:
        click.echo(f"Retrieving: {final_identifier}")
        click.echo(f"Output: {output_dir}")

    result = asyncio.run(retriever.retrieve(
        doi=doi,
        title=title,
        output_dir=output_dir,
        verbose=verbose,
    ))

    if result.status == RetrievalStatus.SUCCESS:
        click.echo(click.style("✓ Downloaded: ", fg="green") + str(result.pdf_path))
        click.echo(f"  Source: {result.source}")
        if result.metadata and result.metadata.get("title"):
            click.echo(f"  Title: {_safe_str(result.metadata['title'])}")
    elif result.status == RetrievalStatus.SKIPPED:
        click.echo(click.style("⊘ Skipped: ", fg="yellow") + "Already exists")
        click.echo(f"  Path: {result.pdf_path}")
    else:
        click.echo(click.style("✗ Failed: ", fg="red") + str(result.error), err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", default=None, help="Output directory (uses config if not set)")
@click.option("--email", envvar="PAPER_EMAIL", help="Email for API access")
@click.option("--s2-key", envvar="S2_API_KEY", help="Semantic Scholar API key")
@click.option("-n", "--concurrent", default=None, help="Max concurrent downloads (uses config if not set)", type=int)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.pass_context
def batch(
    ctx: click.Context,
    input_file: str,
    output: str | None,
    email: str | None,
    s2_key: str | None,
    concurrent: int | None,
    verbose: bool,
):
    """Batch download papers with multi-source fallback.

    Input formats: JSON array, CSV (with doi/title columns), or text (one ID per line)

    Examples:
        parser batch papers.json -o ./papers
        parser batch dois.txt -o ./papers --concurrent 3
    """
    from .acquisition.config import Config
    from .acquisition.retriever import PaperRetriever, RetrievalStatus

    config = Config.load(ctx.obj.get("config_path"))
    if email:
        config.email = email
    if s2_key:
        config.api_keys["semantic_scholar"] = s2_key

    # Use config values as defaults
    output_dir = Path(output) if output else config.get_output_dir()
    max_concurrent = concurrent if concurrent is not None else config.batch.get("max_concurrent", 3)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load papers from file
    papers = _load_papers_from_file(input_file)
    if not papers:
        click.echo(click.style("No papers found in file", fg="yellow"))
        return

    # Categorize papers with priority: title → DOI → pdf_url → arxiv_id
    # Papers with only pdf_url (no title/DOI) are downloaded directly
    # Papers with title or DOI go through retriever for metadata lookup
    pdf_only = []  # Direct PDF download (no metadata search)
    searchable = []  # Title or DOI based search

    for p in papers:
        has_title = bool(p.get("title"))
        has_doi = bool(p.get("doi"))
        has_pdf = bool(p.get("pdf_url"))

        if has_title or has_doi:
            # Use title/DOI for search (pdf_url as fallback)
            searchable.append(p)
        elif has_pdf:
            # Only has PDF URL - direct download
            pdf_only.append(p)
        # Skip papers with no identifiable info

    click.echo(f"Found {len(papers)} papers to retrieve:")
    click.echo(f"  - {len(searchable)} with title/DOI (metadata search)")
    click.echo(f"  - {len(pdf_only)} direct PDF URLs")
    if verbose:
        click.echo(f"Output directory: {output_dir}")
        click.echo(f"Max concurrent: {max_concurrent}")

    # Download direct PDF URLs first (papers with only pdf_url)
    from urllib.parse import urlparse

    import httpx

    for i, paper in enumerate(pdf_only, 1):
        pdf_url: str = paper["pdf_url"] or ""
        if verbose:
            click.echo(f"\n[{i}/{len(pdf_only)}] Downloading direct PDF: {pdf_url[:60]}...")

        try:
            parsed = urlparse(pdf_url)
            filename = Path(parsed.path).name
            if not filename.endswith('.pdf'):
                filename = f"downloaded_{hash(pdf_url) % 10000}.pdf"

            output_path = output_dir / filename

            with httpx.Client(follow_redirects=True, timeout=60.0) as client:
                response = client.get(pdf_url)
                response.raise_for_status()
                output_path.write_bytes(response.content)

            click.echo(click.style("✓ Downloaded: ", fg="green") + str(output_path))
        except Exception as e:
            click.echo(click.style("✗ Failed: ", fg="red") + str(e))

    # If no searchable papers left, we're done
    if not searchable:
        return

    retriever = PaperRetriever(config)

    async def run():
        return await retriever.retrieve_batch(
            searchable,
            output_dir=output_dir,
            verbose=verbose,
            max_concurrent=max_concurrent,
        )

    results = asyncio.run(run())

    success = sum(1 for r in results if r.status == RetrievalStatus.SUCCESS)
    skipped = sum(1 for r in results if r.status == RetrievalStatus.SKIPPED)
    failed = sum(1 for r in results if r.status in (RetrievalStatus.NOT_FOUND, RetrievalStatus.FAILED))

    click.echo()
    click.echo("Results:")
    click.echo(click.style(f"  ✓ Downloaded: {success}", fg="green"))
    if skipped:
        click.echo(click.style(f"  ⊘ Skipped: {skipped}", fg="yellow"))
    if failed:
        click.echo(click.style(f"  ✗ Failed: {failed}", fg="red"))

    # List failures
    failures = [r for r in results if r.status == RetrievalStatus.NOT_FOUND]
    if failures:
        click.echo()
        click.echo("Failed papers:")
        for r in failures:
            identifier = r.doi or r.title
            click.echo(f"  - {identifier}")


@cli.command()
@click.pass_context
def sources(ctx: click.Context) -> None:
    """List available sources and their status."""
    from .acquisition.config import Config

    config = Config.load(ctx.obj.get("config_path"))

    click.echo("Available sources:")
    click.echo()

    sorted_sources = sorted(
        config.sources.items(),
        key=lambda x: x[1].get("priority", 99)
    )

    for name, settings in sorted_sources:
        priority = settings.get("priority", 99)
        enabled = settings.get("enabled", False)
        status = click.style("enabled", fg="green") if enabled else click.style("disabled", fg="red")
        click.echo(f"  {priority}. {name}: {status}")

    # Show institutional access status
    click.echo()
    inst = config.institutional
    if inst.get("enabled"):
        click.echo("Institutional access:")
        if inst.get("vpn_enabled"):
            click.echo(click.style("  Mode: VPN", fg="green"))
        elif inst.get("proxy_url"):
            click.echo("  Mode: EZProxy")
            click.echo(f"  Proxy URL: {inst.get('proxy_url')}")

    # Show unofficial sources
    if config.is_unofficial_enabled():
        click.echo()
        click.echo(click.style("Unofficial sources enabled", fg="yellow"))


@cli.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize a configuration file.

    Creates a config.yaml file with default settings.
    """
    config_path = Path(ctx.obj.get("config_path") or "config.yaml")

    if config_path.exists() and not click.confirm(f"{config_path} exists. Overwrite?"):
        return

    default_config = '''# Parser Configuration
# Edit this file to customize settings

# Your email (required for polite API access)
user:
  email: "your.email@university.edu"

# API Keys (optional but recommended)
api_keys:
  ncbi: null  # Get from https://www.ncbi.nlm.nih.gov/account/settings/
  semantic_scholar: null  # Get from https://www.semanticscholar.org/product/api

# Source configuration (ordered by priority)
sources:
  unpaywall:
    enabled: true
    priority: 1
  arxiv:
    enabled: true
    priority: 2
  pmc:
    enabled: true
    priority: 3
  biorxiv:
    enabled: true
    priority: 4
  semantic_scholar:
    enabled: true
    priority: 5
  openalex:
    enabled: true
    priority: 6
  institutional:
    enabled: false
    priority: 7
  web_search:
    enabled: false
    priority: 8
  scihub:
    enabled: false
    priority: 9
  libgen:
    enabled: false
    priority: 10

# Institutional Access (for IEEE, ACM, etc.)
institutional:
  enabled: false
  vpn_enabled: false
  vpn_script: null
  proxy_url: null  # e.g., "https://ezproxy.university.edu/login?url="
  cookies_file: ".institutional_cookies.pkl"

# Unofficial sources (Sci-Hub, LibGen)
unofficial:
  disclaimer_accepted: false  # Set true to enable unofficial sources

# Download settings
download:
  output_dir: "./downloads"
  skip_existing: true
  max_title_length: 50

# Rate limiting (seconds between requests)
rate_limits:
  global_delay: 1.0
  per_source_delays:
    crossref: 0.5
    unpaywall: 0.1
    arxiv: 3.0
    pmc: 0.34
    semantic_scholar: 3.0
    biorxiv: 1.0

# Batch processing
batch:
  max_concurrent: 3
  retry_failed: true
  max_retries: 2
  progress_file: ".retrieval_progress.json"
'''

    config_path.write_text(default_config)
    click.echo(f"Created {config_path}")
    click.echo("Please edit the file and set your email address.")


@cli.command()
@click.pass_context
def auth(ctx: click.Context) -> None:
    """Authenticate with your institution for access to IEEE, ACM, etc.

    Two modes:
    1. VPN Mode: Configure vpn_enabled: true and vpn_script
    2. EZProxy Mode: Configure proxy_url, then run this command
    """
    from .acquisition.config import Config

    config = Config.load(ctx.obj.get("config_path"))

    if not config.institutional.get("enabled"):
        click.echo(click.style("Error: ", fg="red") + "Institutional access not enabled")
        click.echo()
        click.echo("Add the following to your config.yaml:")
        click.echo("  institutional:")
        click.echo("    enabled: true")
        click.echo('    proxy_url: "https://ezproxy.your-university.edu/login?url="')
        return

    inst = config.institutional

    # VPN mode
    if inst.get("vpn_enabled"):
        vpn_script = inst.get("vpn_script")
        if not vpn_script:
            click.echo(click.style("Error: ", fg="red") + "VPN mode enabled but no vpn_script configured")
            return

        try:
            from .acquisition.clients.institutional import InstitutionalAccessClient
            client = InstitutionalAccessClient(vpn_enabled=True, vpn_script=vpn_script)
            success = client.connect_vpn()
            if success:
                click.echo(click.style("Success! ", fg="green") + "VPN connected")
            else:
                click.echo(click.style("VPN connection failed", fg="red"))
        except Exception as e:
            click.echo(click.style("Error: ", fg="red") + str(e))
        return

    # EZProxy mode
    if not inst.get("proxy_url"):
        click.echo(click.style("Error: ", fg="red") + "No proxy_url configured")
        return

    try:
        from .acquisition.clients.institutional import InstitutionalAccessClient
        client = InstitutionalAccessClient(
            proxy_url=inst.get("proxy_url"),
            vpn_enabled=False,
            cookies_file=inst.get("cookies_file", ".institutional_cookies.pkl"),
        )
        success = client.authenticate_interactive()
        if success:
            click.echo(click.style("Success! ", fg="green") + "Authenticated")
        else:
            click.echo(click.style("Authentication failed", fg="red"))
    except ImportError as e:
        click.echo(click.style("Error: ", fg="red") + str(e))
        click.echo("Install Selenium with: pip install selenium webdriver-manager")


@cli.group()
def config() -> None:
    """Manage configuration sync across machines."""
    pass


@config.command("push")
@click.option("--gist-id", help="Existing gist ID to update")
@click.pass_context
def config_push(ctx: click.Context, gist_id: str | None) -> None:
    """Push config to a private GitHub gist.

    Requires GitHub CLI (gh) to be installed and authenticated.
    """
    import subprocess

    config_path = Path(ctx.obj.get("config_path") or "config.yaml")
    gist_id_file = Path(".parser_gist_id")

    if not config_path.exists():
        click.echo(click.style("Error: ", fg="red") + f"Config file not found: {config_path}")
        return

    # Check gh is available
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo(click.style("Error: ", fg="red") + "GitHub CLI (gh) not found")
        click.echo("Install from: https://cli.github.com/")
        return

    if not gist_id and gist_id_file.exists():
        gist_id = gist_id_file.read_text().strip()

    if gist_id:
        # Update existing gist
        click.echo(f"Updating gist {gist_id}...")
        result = subprocess.run(
            ["gh", "gist", "edit", gist_id, "-f", str(config_path)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            click.echo(click.style("Error: ", fg="red") + result.stderr)
            return
        click.echo(click.style("Success! ", fg="green") + f"Config updated in gist {gist_id}")
    else:
        # Create new gist
        click.echo("Creating new private gist...")
        result = subprocess.run(
            ["gh", "gist", "create", str(config_path), "--desc", "parser config"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            click.echo(click.style("Error: ", fg="red") + result.stderr)
            return

        gist_url = result.stdout.strip()
        new_gist_id = gist_url.split("/")[-1]
        gist_id_file.write_text(new_gist_id)

        click.echo(click.style("Success! ", fg="green") + f"Config uploaded to: {gist_url}")


@config.command("pull")
@click.option("--gist-id", help="Gist ID to pull from")
@click.pass_context
def config_pull(ctx: click.Context, gist_id: str | None) -> None:
    """Pull config from a private GitHub gist."""
    import subprocess

    config_path = Path(ctx.obj.get("config_path") or "config.yaml")
    gist_id_file = Path(".parser_gist_id")

    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo(click.style("Error: ", fg="red") + "GitHub CLI (gh) not found")
        return

    if not gist_id:
        if gist_id_file.exists():
            gist_id = gist_id_file.read_text().strip()
        else:
            click.echo(click.style("Error: ", fg="red") + "No gist ID provided or saved")
            return

    click.echo(f"Pulling config from gist {gist_id}...")

    result = subprocess.run(
        ["gh", "gist", "view", gist_id, "-r"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        click.echo(click.style("Error: ", fg="red") + result.stderr)
        return

    # Backup existing
    if config_path.exists():
        backup_path = config_path.with_suffix(".yaml.bak")
        config_path.rename(backup_path)
        click.echo(f"Backed up existing config to {backup_path}")

    config_path.write_text(result.stdout)
    gist_id_file.write_text(gist_id)

    click.echo(click.style("Success! ", fg="green") + f"Config saved to {config_path}")


# =============================================================================
# Commands from doi2bib
# =============================================================================

@cli.command()
@click.argument("identifier", required=False)
@click.option("-i", "--input", "input_file", type=click.Path(exists=True), help="File with DOIs (txt, json from parse-refs)")
@click.option("-o", "--output", "output_file", type=click.Path(), help="Output file")
@click.option("--format", "output_format", type=click.Choice(["bibtex", "json", "markdown"]), default="bibtex", help="Output format")
@click.option("--email", envvar="PAPER_EMAIL", help="Email for API access")
@click.option("--s2-key", envvar="S2_API_KEY", help="Semantic Scholar API key")
def doi2bib(
    identifier: str | None,
    input_file: str | None,
    output_file: str | None,
    output_format: str,
    email: str | None,
    s2_key: str | None,
):
    """Convert DOI or arXiv ID to BibTeX/JSON/Markdown.

    Simple lookup - provide a DOI or arXiv ID, get metadata back.
    Can also process a file of DOIs.

    Input file formats:
    - TXT: One DOI/arXiv ID per line (dois.txt from parse-refs)
    - JSON: Array of {doi, title, arxiv_id} objects (batch.json from parse-refs)

    Priority: title → DOI → arxiv_id (searches by best available identifier)

    Examples:
        parser doi2bib 10.1038/nature12373
        parser doi2bib arXiv:1605.08695 --format json
        parser doi2bib 1912.01703 --format markdown
        parser doi2bib -i dois.txt -o references.bib
        parser doi2bib -i batch.json -o references.bib
    """
    from .doi2bib.metadata import get_metadata as fetch_metadata
    from .doi2bib.resolver import resolve_identifier

    async def get_metadata(ident_str: str):
        ident = resolve_identifier(ident_str)
        return await fetch_metadata(ident, email=email, s2_api_key=s2_key)

    def format_result(result) -> str:
        if output_format == "bibtex":
            return result.to_bibtex()
        elif output_format == "markdown":
            return result.to_markdown()
        else:
            return json.dumps(result.to_dict(), indent=2, default=str)

    # File mode
    if input_file:
        path = Path(input_file)
        identifiers = []

        # Support both JSON (batch.json) and TXT (dois.txt) formats
        if path.suffix == ".json":
            with open(path) as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            identifiers.append(item)
                        elif isinstance(item, dict):
                            # Priority: title → DOI → arxiv_id
                            # For doi2bib, we need DOI/arXiv, but title can help with search
                            if item.get("doi"):
                                identifiers.append(item["doi"])
                            elif item.get("arxiv_id"):
                                arxiv = item["arxiv_id"]
                                if not arxiv.lower().startswith("arxiv:"):
                                    arxiv = f"arXiv:{arxiv}"
                                identifiers.append(arxiv)
                            elif item.get("title"):
                                # Title-based search not supported in doi2bib
                                click.echo(f"  Skipping (title only, no DOI): {item['title'][:50]}...", err=True)
        else:
            # TXT format - one identifier per line
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        identifiers.append(line)

        if not identifiers:
            click.echo("No DOIs/arXiv IDs found in file", err=True)
            sys.exit(1)

        click.echo(f"Processing {len(identifiers)} identifiers...", err=True)
        results = []
        failed = []
        for ident in identifiers:
            click.echo(f"  {ident}...", err=True)
            result = asyncio.run(get_metadata(ident))
            if result:
                results.append(format_result(result))
            else:
                failed.append(ident)
                click.echo("    ✗ Failed", err=True)

        separator = "\n\n" if output_format == "bibtex" else "\n---\n"
        output = separator.join(results)

        if output_file:
            Path(output_file).write_text(output)
            click.echo(f"\n✓ Wrote {len(results)} entries to {output_file}", err=True)
            if failed:
                click.echo(f"✗ Failed: {len(failed)} identifiers", err=True)
        else:
            click.echo(output)
        return

    # Single identifier mode
    if not identifier:
        click.echo("Error: Provide an identifier or use -i for file input", err=True)
        sys.exit(1)

    result = asyncio.run(get_metadata(identifier))

    if not result:
        click.echo(f"Could not find: {identifier}", err=True)
        sys.exit(1)

    formatted = format_result(result)

    if output_file:
        Path(output_file).write_text(formatted)
        click.echo(f"Wrote to {output_file}", err=True)
    else:
        click.echo(formatted)


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output", default=None, help="Output directory")
@click.option("--email", envvar="PAPER_EMAIL", help="Email for CrossRef")
@click.option("--skip-keys", default=None, help="Comma-separated keys to skip verification")
@click.option("--skip-keys-file", type=click.Path(exists=True), help="File with keys to skip (one per line)")
@click.option("--manual", "manual_path", type=click.Path(exists=True), help="Manual.bib with pre-verified entries")
@click.option("--dry-run", is_flag=True, help="Don't write files, just show what would happen")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def verify(
    input_path: str,
    output: str | None,
    email: str | None,
    skip_keys: str | None,
    skip_keys_file: str | None,
    manual_path: str | None,
    dry_run: bool,
    verbose: bool,
):
    """Verify BibTeX citations against CrossRef and arXiv.

    Supports both single file and directory mode:
    - Single file: Outputs verified.bib, failed.bib, report.md
    - Directory: Outputs verified/*.bib, failed/*.bib, report.md

    Examples:
        parser verify references.bib -o ./output
        parser verify citations_dir/ -o ./output
        parser verify refs.bib --skip-keys "manual1,manual2"
        parser verify refs.bib --skip-keys-file skip.txt
        parser verify refs.bib --manual manual.bib --dry-run
    """
    from .doi2bib.verifier import CitationVerifier

    input_p = Path(input_path)
    output_dir = Path(output) if output else input_p.parent if input_p.is_file() else input_p.parent / "output"

    # Build skip set from --skip-keys and --skip-keys-file
    skip_set: set[str] = set()
    if skip_keys:
        skip_set.update(skip_keys.split(","))
    if skip_keys_file:
        skip_file_path = Path(skip_keys_file)
        for line in skip_file_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                skip_set.add(line)
    manual_p = Path(manual_path) if manual_path else None

    verifier = CitationVerifier(email=email)

    if input_p.is_dir():
        # Directory mode
        click.echo("=" * 60)
        click.echo("Citation Verification (Directory Mode)")
        click.echo("=" * 60)
        click.echo(f"Input: {input_p}")
        click.echo(f"Output: {output_dir}")
        if skip_set:
            click.echo(f"Skipping keys: {', '.join(skip_set)}")
        if dry_run:
            click.echo(click.style("[DRY RUN]", fg="yellow"))
        click.echo()

        async def run_dir():
            return await verifier.verify_directory(
                input_p, output_dir, skip_keys=skip_set, dry_run=dry_run
            )

        stats, results = asyncio.run(run_dir())
    else:
        # Single file mode
        click.echo("=" * 60)
        click.echo("Citation Verification (Single File Mode)")
        click.echo("=" * 60)
        click.echo(f"Input: {input_p}")
        click.echo(f"Output: {output_dir}")
        if skip_set:
            click.echo(f"Skipping keys: {', '.join(skip_set)}")
        if manual_p:
            click.echo(f"Manual entries: {manual_p}")
        if dry_run:
            click.echo(click.style("[DRY RUN]", fg="yellow"))
        click.echo()

        async def run_file():
            return await verifier.verify_file(
                input_p, output_dir, skip_keys=skip_set, manual_path=manual_p, dry_run=dry_run
            )

        stats, results = asyncio.run(run_file())

    # Print results
    click.echo()
    click.echo("Results:")
    click.echo(f"  Verified: {stats.verified}")
    click.echo(f"  arXiv: {stats.arxiv}")
    click.echo(f"  Searched: {stats.searched}")
    click.echo(f"  Website: {stats.website}")
    click.echo(f"  Manual: {stats.manual}")
    click.echo(click.style(f"  Failed: {stats.failed}", fg="red" if stats.failed else None))
    click.echo()
    click.echo(f"Total verified: {stats.total_verified}")
    click.echo(f"Total failed: {stats.failed}")

    if not dry_run:
        click.echo()
        click.echo(f"Output written to: {output_dir}")


# =============================================================================
# New commands (ingestor)
# =============================================================================

@cli.command("parse-refs")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", default=None, help="Output directory")
@click.option("--format", "output_format", type=click.Choice(["json", "md", "both"]), default="both")
@click.option(
    "--agent",
    "agent_type",
    type=click.Choice(["none", "claude", "anthropic", "gemini", "google"]),
    default="none",
    help="AI agent: claude (SDK, no API key), anthropic (API key), gemini (SDK), google (API key)"
)
@click.option("--api-key", default=None, help="API key for agent (not needed for claude-sdk)")
@click.option("--model", default=None, help="Model to use for agent parsing")
@click.option("--compare", is_flag=True, help="Run both regular and agent parsing for comparison")
@click.option("--export-batch", is_flag=True, help="Export JSON for 'parser batch' (DOIs, arXiv, PDFs)")
@click.option("--export-dois", is_flag=True, help="Export DOI/arXiv IDs for 'parser doi2bib -i'")
def parse_refs(
    input_file: str,
    output: str | None,
    output_format: str,
    agent_type: str,
    api_key: str | None,
    model: str | None,
    compare: bool,
    export_batch: bool,
    export_dois: bool,
):
    """Parse references from a research document.

    Extracts DOIs, arXiv IDs, GitHub repos, YouTube videos, etc.

    Modes:
    - Regular (default): Fast regex-based extraction
    - Agent: AI-powered extraction using Claude or Gemini
    - Compare: Run both and compare results

    Agent Options (Claude):
    - claude: Uses Claude Agent SDK (NO API KEY needed - uses Claude Code CLI)
    - anthropic: Direct Anthropic API (requires ANTHROPIC_API_KEY)

    Agent Options (Google):
    - gemini: Uses Google ADK (requires GOOGLE_API_KEY)
    - google: Direct google-generativeai API (requires GOOGLE_API_KEY)

    Export Options:
    - --export-batch: Output batch.json for 'parser batch' (papers with DOIs/arXiv/PDFs)
    - --export-dois: Output dois.txt for 'parser doi2bib -i' (DOI/arXiv IDs only)

    Examples:
        # Regular parsing (regex-based)
        parser parse-refs research_report.md
        parser parse-refs report.md -o ./refs --format json

        # Agent-based parsing with Claude SDK (NO API KEY!)
        parser parse-refs report.md --agent claude

        # Agent with direct Anthropic API (needs API key)
        ANTHROPIC_API_KEY=xxx parser parse-refs report.md --agent anthropic

        # Agent-based parsing with Google ADK
        GOOGLE_API_KEY=xxx parser parse-refs report.md --agent gemini

        # Agent with direct Google API (needs API key)
        GOOGLE_API_KEY=xxx parser parse-refs report.md --agent google

        # Compare regular vs agent parsing
        parser parse-refs report.md --compare --agent claude

        # Export for acquisition pipeline
        parser parse-refs report.md --export-batch --export-dois
        parser batch batch.json -o ./papers  # Download extracted papers
        parser doi2bib -i dois.txt -o refs.bib  # Generate BibTeX
    """
    from .parser import ResearchParser
    input_path = Path(input_file)
    base_output_dir = Path(output) if output else input_path.parent

    # Determine which parsing modes to run
    run_regular = agent_type == "none" or compare
    run_agent = agent_type != "none"

    results = {}

    # Run regular parsing
    if run_regular:
        click.echo("=" * 60)
        click.echo("Running REGULAR (regex-based) parsing...")
        click.echo("=" * 60)

        regular_output_dir = base_output_dir / "regular" if compare else base_output_dir
        regular_output_dir.mkdir(parents=True, exist_ok=True)

        parser = ResearchParser()
        refs = parser.parse_file(input_path)
        results["regular"] = refs

        if refs:
            grouped = parser.group_by_type(refs)
            _save_references(refs, grouped, regular_output_dir, output_format, "regular" if compare else "")

            # Export for batch/doi2bib
            if export_batch:
                _export_for_batch(refs, regular_output_dir, "regular" if compare else "")
            if export_dois:
                _export_for_doi2bib(refs, regular_output_dir, "regular" if compare else "")

            click.echo(f"\nFound {len(refs)} references (regular):")
            for ref_type, type_refs in grouped.items():
                click.echo(f"  {ref_type.value}: {len(type_refs)}")
        else:
            click.echo("No references found (regular).", err=True)

    # Run agent parsing
    if run_agent:
        click.echo("\n" + "=" * 60)
        click.echo(f"Running AGENT ({agent_type}) parsing...")
        click.echo("=" * 60)

        try:
            from .agent import create_agent, is_agent_available

            # Check if agent is available
            available, msg = is_agent_available(agent_type)  # type: ignore[arg-type]
            if not available:
                click.echo(f"Error: {msg}", err=True)
                sys.exit(1)

            agent_output_dir = base_output_dir / "agent" if compare else base_output_dir
            agent_output_dir.mkdir(parents=True, exist_ok=True)

            # Create agent
            agent = create_agent(agent_type, api_key=api_key, model=model)  # type: ignore[arg-type]
            click.echo(f"Using model: {agent.model}")

            # Parse
            result = agent.parse_file(input_path)
            results["agent"] = result.references

            if result.references:
                # Group by type
                grouped = {}
                for ref in result.references:
                    if ref.type not in grouped:
                        grouped[ref.type] = []
                    grouped[ref.type].append(ref)

                agent_prefix = f"agent_{agent_type}" if compare else ""
                _save_references(
                    result.references, grouped, agent_output_dir, output_format,
                    agent_prefix
                )

                # Export for batch/doi2bib
                if export_batch:
                    _export_for_batch(result.references, agent_output_dir, agent_prefix)
                if export_dois:
                    _export_for_doi2bib(result.references, agent_output_dir, agent_prefix)

                # Save raw response
                raw_path = agent_output_dir / "agent_raw_response.txt"
                raw_path.write_text(result.raw_response)
                click.echo(f"✓ Raw response: {raw_path}")

                # Save full result with metadata
                result_path = agent_output_dir / "agent_result.json"
                result_path.write_text(json.dumps(result.to_dict(), indent=2))
                click.echo(f"✓ Full result: {result_path}")

                click.echo(f"\nFound {len(result.references)} references (agent):")
                for ref_type, type_refs in grouped.items():
                    click.echo(f"  {ref_type.value}: {len(type_refs)}")

                if result.tokens_used:
                    click.echo(f"\nTokens used: {result.tokens_used}")
            else:
                click.echo("No references found (agent).", err=True)

        except ImportError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

    # Compare results if requested
    if compare and "regular" in results and "agent" in results:
        click.echo("\n" + "=" * 60)
        click.echo("COMPARISON: Regular vs Agent")
        click.echo("=" * 60)

        regular_refs = results["regular"]
        agent_refs = results["agent"]

        # Create sets of (type, value) for comparison
        regular_set = {(r.type.value, r.value.lower()) for r in regular_refs}
        agent_set = {(r.type.value, r.value.lower()) for r in agent_refs}

        common = regular_set & agent_set
        only_regular = regular_set - agent_set
        only_agent = agent_set - regular_set

        click.echo("\nTotal references:")
        click.echo(f"  Regular: {len(regular_refs)}")
        click.echo(f"  Agent: {len(agent_refs)}")
        click.echo("\nOverlap analysis:")
        click.echo(f"  Common: {len(common)}")
        click.echo(f"  Only in Regular: {len(only_regular)}")
        click.echo(f"  Only in Agent: {len(only_agent)}")

        if only_regular:
            click.echo("\nOnly found by Regular parsing:")
            for ref_type, value in sorted(only_regular)[:10]:  # type: ignore[assignment]
                click.echo(f"  [{ref_type}] {value[:60]}...")  # ref_type is already str
            if len(only_regular) > 10:
                click.echo(f"  ... and {len(only_regular) - 10} more")

        if only_agent:
            click.echo("\nOnly found by Agent parsing:")
            for ref_type, value in sorted(only_agent)[:10]:  # type: ignore[assignment]
                click.echo(f"  [{ref_type}] {value[:60]}...")  # ref_type is already str
            if len(only_agent) > 10:
                click.echo(f"  ... and {len(only_agent) - 10} more")

        # Save comparison report
        comparison_path = base_output_dir / "comparison_report.md"
        comparison_lines = [
            "# Parsing Comparison Report\n",
            f"Input: {input_path}\n",
            "\n## Summary\n",
            f"- Regular parsing: {len(regular_refs)} references",
            f"- Agent parsing: {len(agent_refs)} references",
            f"- Common: {len(common)}",
            f"- Only Regular: {len(only_regular)}",
            f"- Only Agent: {len(only_agent)}",
            "\n## Only in Regular Parsing\n",
        ]
        for ref_type, value in sorted(only_regular):  # type: ignore[assignment]
            comparison_lines.append(f"- [{ref_type}] {value}")
        comparison_lines.append("\n## Only in Agent Parsing\n")
        for ref_type, value in sorted(only_agent):  # type: ignore[assignment]
            comparison_lines.append(f"- [{ref_type}] {value}")

        comparison_path.write_text("\n".join(comparison_lines))
        click.echo(f"\n✓ Comparison report: {comparison_path}")


def _save_references(refs, grouped, output_dir: Path, output_format: str, prefix: str = ""):
    """Save references to files."""
    name_prefix = f"{prefix}_" if prefix else ""

    if output_format in ("json", "both"):
        json_path = output_dir / f"{name_prefix}references.json"
        json_path.write_text(json.dumps([
            {"type": r.type.value, "value": r.value, "title": r.title,
             "authors": r.authors, "year": r.year, "url": r.url, "metadata": r.metadata}
            for r in refs
        ], indent=2))
        click.echo(f"✓ JSON: {json_path}")

    if output_format in ("md", "both"):
        md_path = output_dir / f"{name_prefix}references.md"
        md_lines = ["# Extracted References\n"]
        for ref_type, type_refs in grouped.items():
            md_lines.append(f"\n## {ref_type.value.title()} ({len(type_refs)})\n")
            for r in type_refs:
                line = f"- [{r.value}]({r.url})" if r.url else f"- {r.value}"
                md_lines.append(line)
                if r.title and r.title != r.value:
                    md_lines.append(f"  - {r.title}")
        md_path.write_text("\n".join(md_lines))
        click.echo(f"✓ Markdown: {md_path}")


def _export_for_batch(refs, output_dir: Path, prefix: str = ""):
    """Export references for 'parser batch' command.

    Creates a JSON file with format: [{"doi": ..., "title": ..., "pdf_url": ..., "arxiv_id": ...}, ...]
    Merges entries by title to avoid duplicates and collect all metadata.
    Filters out problematic DOIs (peer reviews, book chapters, etc.)
    """
    from .parser import ReferenceType
    from .validation import is_problematic_doi

    name_prefix = f"{prefix}_" if prefix else ""
    skipped_dois = []  # Track problematic DOIs for reporting

    # First pass: collect all metadata by title (normalized) and PDF URL
    papers_by_title: dict[str, dict] = {}
    papers_by_pdf_url: dict[str, str] = {}  # Map PDF URL to normalized title

    def normalize_title(title: str) -> str:
        """Normalize title for deduplication."""
        if not title:
            return ""
        # Lowercase, remove extra whitespace, common punctuation
        import re
        title = title.lower().strip()
        title = re.sub(r'[:\\-–—]', ' ', title)
        title = re.sub(r'\\s+', ' ', title)
        return title

    def update_paper(norm_title: str, title: str, doi: str | None = None,
                     pdf_url: str | None = None, arxiv_id: str | None = None):
        """Update or create paper entry, preserving best metadata."""
        # Check if DOI is problematic (peer review, book chapter, etc.)
        if doi:
            is_problematic, reason = is_problematic_doi(doi)
            if is_problematic:
                skipped_dois.append({"doi": doi, "title": title, "reason": reason})
                doi = None  # Don't use this DOI

        # If PDF URL exists, check if we already have this paper under a different title
        if pdf_url and pdf_url in papers_by_pdf_url:
            # Merge with existing entry
            norm_title = papers_by_pdf_url[pdf_url]

        if norm_title not in papers_by_title:
            papers_by_title[norm_title] = {
                "title": title,
                "doi": None,
                "pdf_url": None,
                "arxiv_id": None
            }
            # Register PDF URL if provided
            if pdf_url:
                papers_by_pdf_url[pdf_url] = norm_title

        paper = papers_by_title[norm_title]
        # Keep longest/most complete title
        if title and (not paper["title"] or len(title) > len(paper["title"])):
            paper["title"] = title
        # Update DOI (prefer non-arXiv DOI)
        if doi and (not paper["doi"] or (paper["doi"].startswith("10.48550/arXiv") and not doi.startswith("10.48550/arXiv"))):
            paper["doi"] = doi
        # Update PDF URL
        if pdf_url and pdf_url.endswith(".pdf") and not paper["pdf_url"]:
            paper["pdf_url"] = pdf_url
        # Update arXiv ID
        if arxiv_id and not paper["arxiv_id"]:
            paper["arxiv_id"] = arxiv_id

    # Process all references
    for ref in refs:
        title = ref.title or ""
        norm_title = normalize_title(title)

        if ref.type == ReferenceType.DOI:
            doi = ref.value
            title = ref.title or ""
            norm_title = normalize_title(title) if title else doi  # Use DOI as key if no title
            update_paper(norm_title, title, doi=doi)

        elif ref.type == ReferenceType.ARXIV:
            arxiv_id = ref.value
            if arxiv_id.lower().startswith("arxiv:"):
                arxiv_id = arxiv_id[6:]
            doi = f"10.48550/arXiv.{arxiv_id}"
            pdf_url = ref.url if ref.url and "arxiv.org" in ref.url else None
            title = ref.title or ""
            norm_title = normalize_title(title) if title else arxiv_id
            update_paper(norm_title, title, doi=doi, arxiv_id=arxiv_id, pdf_url=pdf_url)

        elif ref.type == ReferenceType.PDF:
            pdf_url = ref.url or ref.value
            title = ref.title or ""
            if title:
                norm_title = normalize_title(title)
                update_paper(norm_title, title, pdf_url=pdf_url)
            else:
                # Include standalone PDFs with URL as identifier
                # Extract filename from URL for title
                import re
                filename_match = re.search(r'/([^/]+\.pdf)$', pdf_url)
                if filename_match:
                    title = filename_match.group(1).replace('.pdf', '').replace('_', ' ').replace('-', ' ')
                norm_title = pdf_url  # Use URL as unique key
                update_paper(norm_title, title or pdf_url, pdf_url=pdf_url)

        elif ref.type == ReferenceType.PAPER:
            title = ref.title or ref.value
            norm_title = normalize_title(title)
            doi = ref.metadata.get("doi") if ref.metadata else None
            arxiv_id = ref.metadata.get("arxiv_id") if ref.metadata else None
            pdf_url = ref.metadata.get("pdf_url") if ref.metadata else None
            # Also check the url field if it's a PDF
            if not pdf_url and ref.url and ref.url.endswith(".pdf"):
                pdf_url = ref.url
            if norm_title:
                update_paper(norm_title, title, doi=doi, pdf_url=pdf_url, arxiv_id=arxiv_id)

    # Convert to list, filter out empty entries
    batch_items = []
    for paper in papers_by_title.values():
        # Skip entries with no useful data
        if not paper["title"] and not paper["doi"] and not paper["pdf_url"]:
            continue
        batch_items.append(paper)

    batch_path = output_dir / f"{name_prefix}batch.json"
    batch_path.write_text(json.dumps(batch_items, indent=2))
    click.echo(f"✓ Batch export ({len(batch_items)} papers): {batch_path}")
    click.echo(f"  Use with: parser batch {batch_path} -o ./papers")

    # Report skipped problematic DOIs
    if skipped_dois:
        click.echo(f"⚠ Skipped {len(skipped_dois)} problematic DOIs:")
        for item in skipped_dois[:5]:  # Show first 5
            doi = item.get('doi', '') or ''
            reason = item.get('reason', '') or ''
            click.echo(f"  - {doi[:50]}...")
            click.echo(f"    Reason: {reason[:80]}...")
        if len(skipped_dois) > 5:
            click.echo(f"  ... and {len(skipped_dois) - 5} more")

        # Save skipped DOIs to file
        skipped_path = output_dir / f"{name_prefix}skipped_dois.json"
        skipped_path.write_text(json.dumps(skipped_dois, indent=2))
        click.echo(f"  Full list saved to: {skipped_path}")

    return batch_path


def _export_for_doi2bib(refs, output_dir: Path, prefix: str = ""):
    """Export DOI/arXiv IDs for 'parser doi2bib -i' command.

    Creates a text file with one identifier per line.
    Includes both DOIs and arXiv IDs.
    """
    from .parser import ReferenceType

    name_prefix = f"{prefix}_" if prefix else ""
    identifiers = []
    seen = set()

    for ref in refs:
        identifier = None

        if ref.type == ReferenceType.DOI:
            identifier = ref.value

        elif ref.type == ReferenceType.ARXIV:
            arxiv_id = ref.value
            if arxiv_id.lower().startswith("arxiv:"):
                arxiv_id = arxiv_id[6:]
            identifier = f"arXiv:{arxiv_id}"

        elif ref.type == ReferenceType.PAPER:
            # Check for DOI or arXiv ID in metadata
            if ref.metadata.get("doi"):
                identifier = ref.metadata["doi"]
            elif ref.metadata.get("arxiv_id"):
                arxiv_id = ref.metadata["arxiv_id"]
                if arxiv_id.lower().startswith("arxiv:"):
                    arxiv_id = arxiv_id[6:]
                identifier = f"arXiv:{arxiv_id}"

        if identifier and identifier not in seen:
            seen.add(identifier)
            identifiers.append(identifier)

    dois_path = output_dir / f"{name_prefix}dois.txt"
    dois_path.write_text("\n".join(identifiers) + "\n")
    click.echo(f"✓ DOI export ({len(identifiers)} identifiers): {dois_path}")
    click.echo(f"  Use with: parser doi2bib -i {dois_path} -o references.bib")

    return dois_path


@cli.command()
@click.argument("identifier")
@click.option("--s2-key", envvar="S2_API_KEY", help="Semantic Scholar API key")
@click.option("--direction", type=click.Choice(["citations", "references", "both"]), default="both")
@click.option("-n", "--limit", default=50, help="Maximum items to retrieve")
@click.option("-o", "--output", default=None, help="Output file (prints to stdout if not specified)")
@click.option("--format", "output_format", type=click.Choice(["json", "text", "bibtex"]), default="text")
def citations(
    identifier: str,
    s2_key: str | None,
    direction: str,
    limit: int,
    output: str | None,
    output_format: str,
):
    """Get citation graph for a paper.

    Retrieves papers that cite this paper (citations) and/or papers
    referenced by this paper (references) via Semantic Scholar API.

    Examples:
        parser citations "arXiv:2005.11401" --direction both
        parser citations "10.1038/nature12373" --direction citations -n 100
        parser citations "10.1038/nature12373" --format bibtex -o refs.bib
    """
    from .acquisition.clients import SemanticScholarClient
    from .doi2bib.resolver import resolve_identifier

    ident = resolve_identifier(identifier)
    s2 = SemanticScholarClient(api_key=s2_key)

    # Build paper ID for Semantic Scholar
    if ident.doi:
        paper_id = f"DOI:{ident.doi}"
    elif ident.arxiv_id:
        paper_id = f"ARXIV:{ident.arxiv_id}"
    else:
        paper_id = ident.value

    async def fetch():
        results: dict[str, Any] = {"paper_id": paper_id, "citations": [], "references": []}

        if direction in ("citations", "both"):
            click.echo(f"Fetching citations for {paper_id}...", err=True)
            results["citations"] = await s2.get_citations(paper_id, limit=limit)
            click.echo(f"  Found {len(results['citations'])} citing papers", err=True)

        if direction in ("references", "both"):
            click.echo(f"Fetching references for {paper_id}...", err=True)
            results["references"] = await s2.get_references(paper_id, limit=limit)
            click.echo(f"  Found {len(results['references'])} referenced papers", err=True)

        return results

    results = asyncio.run(fetch())

    # Format output
    if output_format == "json":
        content = json.dumps(results, indent=2, default=str)
    elif output_format == "bibtex":
        entries = []
        for i, paper in enumerate(results.get("citations", []) + results.get("references", [])):
            if paper.get("title"):
                # Generate simple BibTeX entry
                authors = " and ".join(paper.get("authors", [])[:5])
                key = f"paper{i+1}"
                entry = f"@misc{{{key},\n"
                entry += f"  title = {{{paper.get('title')}}},\n"
                if authors:
                    entry += f"  author = {{{authors}}},\n"
                if paper.get("year"):
                    entry += f"  year = {{{paper['year']}}},\n"
                if paper.get("doi"):
                    entry += f"  doi = {{{paper['doi']}}},\n"
                entry += "}"
                entries.append(entry)
        content = "\n\n".join(entries)
    else:  # text
        lines = []
        if results.get("citations"):
            lines.append(f"# Papers citing this work ({len(results['citations'])})")
            lines.append("")
            for i, paper in enumerate(results["citations"], 1):
                authors = ", ".join(paper.get("authors", [])[:3])
                if len(paper.get("authors", [])) > 3:
                    authors += " et al."
                year = paper.get("year", "n.d.")
                doi = paper.get("doi", "")
                doi_str = f" DOI:{doi}" if doi else ""
                lines.append(f"{i}. {authors} ({year}). {paper.get('title', 'Unknown')}.{doi_str}")
            lines.append("")

        if results.get("references"):
            lines.append(f"# Papers referenced by this work ({len(results['references'])})")
            lines.append("")
            for i, paper in enumerate(results["references"], 1):
                authors = ", ".join(paper.get("authors", [])[:3])
                if len(paper.get("authors", [])) > 3:
                    authors += " et al."
                year = paper.get("year", "n.d.")
                doi = paper.get("doi", "")
                doi_str = f" DOI:{doi}" if doi else ""
                lines.append(f"{i}. {authors} ({year}). {paper.get('title', 'Unknown')}.{doi_str}")

        content = "\n".join(lines)

    # Output
    if output:
        Path(output).write_text(content)
        click.echo(f"Written to {output}")
    else:
        click.echo(content)


# =============================================================================
# Helper functions
# =============================================================================

def _parse_identifier(ident: str) -> tuple[str | None, str | None, str | None]:
    """Parse identifier string to (doi, title, pdf_url) tuple.

    Returns:
        (doi, title, pdf_url) tuple - doi is set for DOI or arXiv identifiers,
        title is set if it looks like a paper title,
        pdf_url is set if it's a direct PDF URL
    """
    ident = ident.strip()

    # Direct PDF URL
    if re.match(r'^https?://.*\.pdf(?:\?.*)?$', ident, re.IGNORECASE):
        return None, None, ident

    # DOI format: 10.xxxx/... or doi:10.xxxx/...
    if re.match(r'^10\.\d{4,}/', ident) or ident.lower().startswith('doi:'):
        return ident.replace("doi:", "").replace("DOI:", "").strip(), None, None

    # arXiv format: arXiv:YYMM.NNNNN or just YYMM.NNNNN
    arxiv_match = re.match(r'^(?:arXiv[:\s]*)?(\d{4}\.\d{4,5})(?:v\d+)?$', ident, re.IGNORECASE)
    if arxiv_match:
        arxiv_id = arxiv_match.group(1)
        # Return as DOI format so it's recognized
        return f"10.48550/arXiv.{arxiv_id}", None, None

    # arxiv.org URL
    arxiv_url_match = re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})', ident, re.IGNORECASE)
    if arxiv_url_match:
        arxiv_id = arxiv_url_match.group(1)
        return f"10.48550/arXiv.{arxiv_id}", None, None

    # Otherwise treat as title
    return None, ident, None


def _safe_str(text: str) -> str:
    """Convert text to ASCII-safe string for Windows console."""
    try:
        text.encode("cp1252")
        return text
    except (UnicodeEncodeError, LookupError):
        return text.encode("ascii", errors="replace").decode("ascii")


def _load_papers_from_file(filepath: str) -> list[dict[str, str | None]]:
    """Load paper identifiers from file.

    Supports multiple input formats:
    - JSON: Array of {doi, title, pdf_url, arxiv_id} objects (from parse-refs --export batch)
    - CSV: With doi,title columns
    - TXT: One identifier per line (DOI, arXiv ID, URL, or title)

    Priority for retrieval: title (for metadata search) → DOI → pdf_url → arxiv_id
    """
    import csv

    path = Path(filepath)
    papers = []

    if path.suffix == ".json":
        with open(path) as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        doi, title, pdf_url = _parse_identifier(item)
                        papers.append({"doi": doi, "title": title, "pdf_url": pdf_url, "arxiv_id": None})
                    elif isinstance(item, dict):
                        # Handle both formats:
                        # 1. parse-refs format: {"type": "doi/arxiv/...", "value": "...", "title": "...", "url": "..."}
                        # 2. batch format: {"doi": "...", "title": "...", "pdf_url": "...", "arxiv_id": "..."}

                        if "type" in item and "value" in item:
                            # parse-refs format - convert to batch format
                            ref_type = item.get("type", "")
                            value = item.get("value", "")
                            title = item.get("title", "")
                            url = item.get("url", "")

                            doi = None
                            arxiv_id = None
                            pdf_url = None

                            if ref_type == "doi":
                                doi = value
                            elif ref_type == "arxiv":
                                arxiv_id = value
                                # Convert arXiv ID to DOI format
                                arxiv_clean = value
                                if arxiv_clean.lower().startswith("arxiv:"):
                                    arxiv_clean = arxiv_clean[6:]
                                doi = f"10.48550/arXiv.{arxiv_clean}"
                            elif ref_type == "website" and url.endswith(".pdf"):
                                pdf_url = url
                            # Skip github, website (non-PDF), etc.
                            elif ref_type in ("github", "website"):
                                continue

                            papers.append({
                                "doi": doi,
                                "title": title,
                                "pdf_url": pdf_url,
                                "arxiv_id": arxiv_id
                            })
                        else:
                            # batch format - use directly
                            doi = item.get("doi")
                            title = item.get("title")
                            pdf_url = item.get("pdf_url")
                            arxiv_id = item.get("arxiv_id")

                            # Convert arXiv ID to DOI format if no DOI present
                            if arxiv_id and not doi:
                                arxiv_clean = arxiv_id
                                if arxiv_clean.lower().startswith("arxiv:"):
                                    arxiv_clean = arxiv_clean[6:]
                                doi = f"10.48550/arXiv.{arxiv_clean}"

                            papers.append({
                                "doi": doi,
                                "title": title,
                                "pdf_url": pdf_url,
                                "arxiv_id": arxiv_id
                            })

    elif path.suffix == ".csv":
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                papers.append({
                    "doi": row.get("doi"),
                    "title": row.get("title"),
                    "pdf_url": row.get("pdf_url"),
                    "arxiv_id": row.get("arxiv_id")
                })

    else:  # txt - one identifier per line
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                doi, title, pdf_url = _parse_identifier(line)
                papers.append({"doi": doi, "title": title, "pdf_url": pdf_url, "arxiv_id": None})

    return papers


def main():
    """Entry point."""
    cli()


if __name__ == "__main__":
    main()
