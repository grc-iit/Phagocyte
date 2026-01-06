"""MCP Server for paper acquisition and reference parsing operations.

This server exposes tools for:
- Retrieving papers by DOI, title, or arXiv ID
- Batch downloading papers
- Parsing references from research documents
- Converting DOIs to BibTeX
- Verifying citations

Usage:
    uv run parser-mcp
"""

import asyncio
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize MCP server
mcp = FastMCP(
    name="parser-mcp",
    instructions="""
Parser MCP Server

Provides tools for scientific paper acquisition, reference parsing, and citation management.

Features:
- Paper retrieval with multi-source fallback (Unpaywall, arXiv, PMC, Semantic Scholar)
- Reference extraction from research documents (regex + AI agent)
- DOI to BibTeX conversion
- Citation verification

Workflow:
1. parse_references - Extract references from a research document
2. retrieve_paper - Download a single paper by DOI/title/arXiv ID
3. batch_retrieve - Download multiple papers from batch file
4. doi_to_bibtex - Convert DOIs to BibTeX format

Tips:
- For best results with parse_references, set agent="claude" for AI-enhanced parsing
- Batch files support JSON, CSV, or plain text (one ID per line)
- Set email for better API access rates
"""
)


# =============================================================================
# Tool Input/Output Models
# =============================================================================


class RetrieveInput(BaseModel):
    """Input for paper retrieval."""

    identifier: str = Field(description="DOI, arXiv ID, or paper title")
    output_dir: str = Field(default="./papers", description="Output directory for PDF")
    email: str | None = Field(default=None, description="Email for API access (improves rate limits)")
    skip_existing: bool = Field(default=True, description="Skip if PDF already exists")
    verbose: bool = Field(default=False, description="Verbose output")


class RetrieveResult(BaseModel):
    """Result of paper retrieval."""

    success: bool
    pdf_path: str | None = None
    source: str | None = None
    title: str | None = None
    error: str | None = None
    skipped: bool = False


class BatchInput(BaseModel):
    """Input for batch paper retrieval."""

    input_file: str = Field(description="Path to batch file (JSON, CSV, or text)")
    output_dir: str = Field(default="./papers", description="Output directory for PDFs")
    email: str | None = Field(default=None, description="Email for API access")
    concurrent: int = Field(default=3, ge=1, le=10, description="Max concurrent downloads")
    verbose: bool = Field(default=False, description="Verbose output")


class BatchResult(BaseModel):
    """Result of batch retrieval."""

    total: int
    succeeded: int
    failed: int
    skipped: int
    results: list[dict]


class ParseRefsInput(BaseModel):
    """Input for reference parsing."""

    input_file: str = Field(description="Path to research document (markdown, text)")
    output_dir: str = Field(default="./parsed", description="Output directory")
    agent: Literal["none", "claude", "gemini"] = Field(
        default="none",
        description="AI agent for enhanced parsing (none=regex only)"
    )
    export_batch: bool = Field(default=True, description="Export batch.json for acquisition")
    export_dois: bool = Field(default=True, description="Export dois.txt file")
    format: Literal["json", "markdown", "both"] = Field(
        default="both",
        description="Output format"
    )


class ParseRefsResult(BaseModel):
    """Result of reference parsing."""

    success: bool
    total_references: int
    json_path: str | None = None
    markdown_path: str | None = None
    batch_path: str | None = None
    dois_path: str | None = None
    agent_used: str
    error: str | None = None


class DoiBibInput(BaseModel):
    """Input for DOI to BibTeX conversion."""

    dois: list[str] = Field(description="List of DOIs to convert")
    output_file: str | None = Field(default=None, description="Output BibTeX file path")


class DoiBibResult(BaseModel):
    """Result of DOI to BibTeX conversion."""

    success: bool
    total: int
    converted: int
    failed: int
    bibtex: str | None = None
    output_path: str | None = None
    errors: list[str] = Field(default_factory=list)


class SourceStatus(BaseModel):
    """Status of paper sources."""

    source: str
    available: bool
    requires_auth: bool
    notes: str | None = None


class VerifyInput(BaseModel):
    """Input for BibTeX verification."""

    input_path: str = Field(description="Path to BibTeX file or directory")
    output_dir: str = Field(default="./verified", description="Output directory")
    skip_keys: list[str] = Field(default_factory=list, description="Citation keys to skip verification")
    email: str | None = Field(default=None, description="Email for CrossRef API")
    dry_run: bool = Field(default=False, description="Don't write files, just report")


class VerifyResult(BaseModel):
    """Result of citation verification."""

    success: bool
    verified: int = 0
    arxiv: int = 0
    searched: int = 0
    website: int = 0
    manual: int = 0
    failed: int = 0
    total_verified: int = 0
    verified_path: str | None = None
    failed_path: str | None = None
    report_path: str | None = None
    error: str | None = None


class CitationsInput(BaseModel):
    """Input for citation graph retrieval."""

    identifier: str = Field(description="DOI or arXiv ID of the paper")
    direction: Literal["citations", "references", "both"] = Field(
        default="both",
        description="Which papers to retrieve: citing this paper, referenced by this paper, or both"
    )
    limit: int = Field(default=50, ge=1, le=1000, description="Maximum papers to retrieve")
    s2_api_key: str | None = Field(default=None, description="Semantic Scholar API key for higher rate limits")


class CitationPaper(BaseModel):
    """A paper in the citation graph."""

    title: str | None = None
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    venue: str | None = None


class CitationsResult(BaseModel):
    """Result of citation graph retrieval."""

    success: bool
    paper_id: str
    citations: list[CitationPaper] = Field(default_factory=list, description="Papers citing this paper")
    references: list[CitationPaper] = Field(default_factory=list, description="Papers referenced by this paper")
    error: str | None = None


# =============================================================================
# Tools
# =============================================================================


@mcp.tool()
async def retrieve_paper(input: RetrieveInput) -> RetrieveResult:
    """Retrieve a single paper PDF by DOI, title, or arXiv ID.

    Tries multiple sources in priority order: Unpaywall, arXiv, PMC, 
    Semantic Scholar, and others.

    Args:
        input: Retrieval configuration

    Returns:
        Result with PDF path and source information

    Example:
        retrieve_paper(identifier="10.1038/nature12373", output_dir="./papers")
        retrieve_paper(identifier="arXiv:2005.11401")
        retrieve_paper(identifier="Attention Is All You Need")
    """
    from parser.acquisition.config import Config
    from parser.acquisition.retriever import PaperRetriever, RetrievalStatus

    config = Config.load()
    if input.email:
        config.email = input.email
    config.download["skip_existing"] = input.skip_existing

    output_dir = Path(input.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    retriever = PaperRetriever(config)

    # Parse identifier to determine DOI vs title
    doi, title = _parse_identifier(input.identifier)

    try:
        result = await retriever.retrieve(
            doi=doi,
            title=title,
            output_dir=output_dir,
            verbose=input.verbose,
        )

        if result.status == RetrievalStatus.SUCCESS:
            return RetrieveResult(
                success=True,
                pdf_path=str(result.pdf_path) if result.pdf_path else None,
                source=result.source,
                title=result.metadata.get("title") if result.metadata else None,
            )
        elif result.status == RetrievalStatus.SKIPPED:
            return RetrieveResult(
                success=True,
                pdf_path=str(result.pdf_path) if result.pdf_path else None,
                skipped=True,
            )
        else:
            return RetrieveResult(
                success=False,
                error=str(result.error) if result.error else "Unknown error",
            )
    except Exception as e:
        return RetrieveResult(success=False, error=str(e))


@mcp.tool()
async def batch_retrieve(input: BatchInput) -> BatchResult:
    """Batch download papers from a file.

    Supports JSON array, CSV (with doi/title columns), or text (one ID per line).

    Args:
        input: Batch retrieval configuration

    Returns:
        Summary of download results

    Example:
        batch_retrieve(input_file="./dois.txt", output_dir="./papers")
        batch_retrieve(input_file="./papers.json", concurrent=5)
    """
    from parser.acquisition.config import Config
    from parser.acquisition.retriever import PaperRetriever, RetrievalStatus

    config = Config.load()
    if input.email:
        config.email = input.email

    output_dir = Path(input.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    retriever = PaperRetriever(config)

    # Load batch file
    input_path = Path(input.input_file)
    if not input_path.exists():
        return BatchResult(
            total=0, succeeded=0, failed=0, skipped=0,
            results=[{"error": f"File not found: {input.input_file}"}]
        )

    items = _load_batch_file(input_path)

    results = []
    succeeded = 0
    failed = 0
    skipped = 0

    # Process with concurrency limit
    semaphore = asyncio.Semaphore(input.concurrent)

    async def process_item(item):
        nonlocal succeeded, failed, skipped
        async with semaphore:
            doi = item.get("doi")
            title = item.get("title")

            try:
                result = await retriever.retrieve(
                    doi=doi,
                    title=title,
                    output_dir=output_dir,
                    verbose=input.verbose,
                )

                if result.status == RetrievalStatus.SUCCESS:
                    succeeded += 1
                    return {"identifier": doi or title, "status": "success", "path": str(result.pdf_path)}
                elif result.status == RetrievalStatus.SKIPPED:
                    skipped += 1
                    return {"identifier": doi or title, "status": "skipped"}
                else:
                    failed += 1
                    return {"identifier": doi or title, "status": "failed", "error": str(result.error)}
            except Exception as e:
                failed += 1
                return {"identifier": doi or title, "status": "failed", "error": str(e)}

    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)

    return BatchResult(
        total=len(items),
        succeeded=succeeded,
        failed=failed,
        skipped=skipped,
        results=list(results),
    )


@mcp.tool()
async def parse_references(input: ParseRefsInput) -> ParseRefsResult:
    """Parse and extract references from a research document.

    Extracts structured citation information including DOIs, arXiv IDs,
    GitHub URLs, and bibliographic metadata.

    Args:
        input: Parsing configuration

    Returns:
        Paths to generated outputs and statistics

    Example:
        parse_references(input_file="./research_report.md", agent="claude")
        parse_references(input_file="./paper.md", export_batch=True)
    """
    import json

    input_path = Path(input.input_file)
    if not input_path.exists():
        return ParseRefsResult(
            success=False,
            total_references=0,
            agent_used=input.agent,
            error=f"File not found: {input.input_file}",
        )

    output_dir = Path(input.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read input document
    content = input_path.read_text(encoding="utf-8")

    try:
        # Use regex parser first
        from parser.parser import ResearchParser
        parser = ResearchParser()
        parsed_refs = parser.parse(content)

        # Convert ParsedReference objects to dicts
        references = []
        for ref in parsed_refs:
            ref_dict = {
                "type": ref.type.value,
                "value": ref.value,
                "title": ref.title,
                "authors": ref.authors,
                "year": ref.year,
                "url": ref.url,
                "context": ref.context,
                "metadata": ref.metadata,
            }
            # Add DOI if available (for DOI type references)
            if ref.type.value == "doi":
                ref_dict["doi"] = ref.value
            # Add arXiv ID if available
            elif ref.type.value == "arxiv":
                ref_dict["arxiv_id"] = ref.value
            references.append(ref_dict)

        # If agent requested, enhance with AI
        if input.agent != "none":
            try:
                if input.agent == "claude":
                    from parser.agent.anthropic_agent import AnthropicAgent
                    agent = AnthropicAgent()
                    references = await agent.enhance_references(content, references)
                elif input.agent == "gemini":
                    from parser.agent.gemini_agent import GeminiAgent
                    agent = GeminiAgent()
                    references = await agent.enhance_references(content, references)
            except ImportError:
                pass  # Fall back to regex only
            except Exception:
                pass  # Fall back to regex only

        result = ParseRefsResult(
            success=True,
            total_references=len(references),
            agent_used=input.agent,
        )

        # Export JSON
        if input.format in ("json", "both"):
            json_path = output_dir / "references.json"
            with open(json_path, "w") as f:
                json.dump(references, f, indent=2)
            result.json_path = str(json_path)

        # Export Markdown
        if input.format in ("markdown", "both"):
            md_path = output_dir / "references.md"
            md_content = _references_to_markdown(references)
            md_path.write_text(md_content)
            result.markdown_path = str(md_path)

        # Export batch file
        if input.export_batch:
            batch_path = output_dir / "batch.json"
            batch_items = [{"doi": r.get("doi"), "title": r.get("title")}
                          for r in references if r.get("doi") or r.get("title")]
            with open(batch_path, "w") as f:
                json.dump(batch_items, f, indent=2)
            result.batch_path = str(batch_path)

        # Export DOIs
        if input.export_dois:
            dois_path = output_dir / "dois.txt"
            dois = [r.get("doi") for r in references if r.get("doi")]
            dois_path.write_text("\n".join(dois))
            result.dois_path = str(dois_path)

        return result

    except Exception as e:
        return ParseRefsResult(
            success=False,
            total_references=0,
            agent_used=input.agent,
            error=str(e),
        )


@mcp.tool()
async def doi_to_bibtex(input: DoiBibInput) -> DoiBibResult:
    """Convert DOIs to BibTeX format.

    Fetches bibliographic metadata from DOI.org and CrossRef,
    then converts to BibTeX entries.

    Args:
        input: DOIs to convert and optional output path

    Returns:
        BibTeX content and conversion statistics

    Example:
        doi_to_bibtex(dois=["10.1038/nature12373", "10.1145/3065386"])
    """
    from parser.doi2bib.metadata import get_metadata
    from parser.doi2bib.resolver import resolve_identifier

    results = []
    errors = []
    bibtex_entries = []

    for identifier in input.dois:
        try:
            # Resolve the identifier
            ident = resolve_identifier(identifier)

            # Get metadata
            metadata = await get_metadata(ident)

            if metadata:
                # Convert to BibTeX
                bib = metadata.to_bibtex()
                bibtex_entries.append(bib)
                results.append(identifier)
            else:
                errors.append(f"{identifier}: No metadata found")
        except Exception as e:
            errors.append(f"{identifier}: {str(e)}")

    bibtex_content = "\n\n".join(bibtex_entries) if bibtex_entries else None

    result = DoiBibResult(
        success=len(results) > 0,
        total=len(input.dois),
        converted=len(results),
        failed=len(errors),
        bibtex=bibtex_content,
        errors=errors,
    )

    # Write to file if requested
    if input.output_file and bibtex_content:
        output_path = Path(input.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(bibtex_content)
        result.output_path = str(output_path)

    return result


@mcp.tool()
async def list_sources() -> list[SourceStatus]:
    """List available paper sources and their status.

    Shows all configured sources for paper retrieval and whether
    they require authentication.

    Returns:
        List of source statuses
    """
    sources = [
        SourceStatus(
            source="unpaywall",
            available=True,
            requires_auth=False,
            notes="Open access papers via DOI. Set email for better rates.",
        ),
        SourceStatus(
            source="arxiv",
            available=True,
            requires_auth=False,
            notes="Preprints from arXiv.org",
        ),
        SourceStatus(
            source="pmc",
            available=True,
            requires_auth=False,
            notes="PubMed Central open access papers",
        ),
        SourceStatus(
            source="semantic_scholar",
            available=True,
            requires_auth=False,
            notes="Set S2_API_KEY for higher rate limits",
        ),
        SourceStatus(
            source="crossref",
            available=True,
            requires_auth=False,
            notes="Metadata and some open access links",
        ),
        SourceStatus(
            source="core",
            available=True,
            requires_auth=True,
            notes="Requires CORE_API_KEY",
        ),
    ]
    return sources


@mcp.tool()
async def verify_citations(input: VerifyInput) -> VerifyResult:
    """Verify BibTeX citations against CrossRef and arXiv.

    Validates each citation entry against authoritative sources
    and classifies them as verified, searched (found by search), 
    or failed.

    Args:
        input: Verification configuration

    Returns:
        Statistics and paths to output files

    Example:
        verify_citations(input_path="./references.bib", output_dir="./verified")
    """
    from parser.doi2bib.verifier import CitationVerifier

    input_path = Path(input.input_path)
    if not input_path.exists():
        return VerifyResult(
            success=False,
            error=f"File not found: {input.input_path}",
        )

    output_dir = Path(input.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    skip_set = set(input.skip_keys)
    verifier = CitationVerifier(email=input.email)

    try:
        if input_path.is_dir():
            # Directory mode
            stats, results = await verifier.verify_directory(
                input_path, output_dir, skip_keys=skip_set, dry_run=input.dry_run
            )
        else:
            # Single file mode
            stats, results = await verifier.verify_file(
                input_path, output_dir, skip_keys=skip_set, dry_run=input.dry_run
            )

        result = VerifyResult(
            success=True,
            verified=stats.verified,
            arxiv=stats.arxiv,
            searched=stats.searched,
            website=stats.website,
            manual=stats.manual,
            failed=stats.failed,
            total_verified=stats.total_verified,
        )

        if not input.dry_run:
            result.verified_path = str(output_dir / "verified.bib")
            result.failed_path = str(output_dir / "failed.bib")
            result.report_path = str(output_dir / "report.md")

        return result

    except Exception as e:
        return VerifyResult(
            success=False,
            error=str(e),
        )


@mcp.tool()
async def get_citations(input: CitationsInput) -> CitationsResult:
    """Get citation graph for a paper via Semantic Scholar.

    Retrieves papers that cite this paper (citations) and/or papers
    that this paper references. Useful for literature review and
    impact analysis.

    Args:
        input: Citation retrieval configuration

    Returns:
        Lists of citing and referenced papers

    Example:
        get_citations(identifier="10.1038/nature12373", direction="both")
        get_citations(identifier="arXiv:2005.11401", direction="citations", limit=100)
    """
    try:
        from parser.acquisition.clients import SemanticScholarClient
        from parser.doi2bib.resolver import resolve_identifier

        ident = resolve_identifier(input.identifier)
        s2 = SemanticScholarClient(api_key=input.s2_api_key)

        # Build paper ID for Semantic Scholar
        if ident.doi:
            paper_id = f"DOI:{ident.doi}"
        elif ident.arxiv_id:
            paper_id = f"ARXIV:{ident.arxiv_id}"
        else:
            paper_id = ident.value

        result = CitationsResult(
            success=True,
            paper_id=paper_id,
        )

        # Fetch citations (papers citing this paper)
        if input.direction in ("citations", "both"):
            citations_raw = await s2.get_citations(paper_id, limit=input.limit)
            result.citations = [
                CitationPaper(
                    title=p.get("title"),
                    authors=p.get("authors", [])[:10],
                    year=p.get("year"),
                    doi=p.get("doi"),
                    arxiv_id=p.get("arxiv_id"),
                    venue=p.get("venue"),
                )
                for p in citations_raw
            ]

        # Fetch references (papers this paper cites)
        if input.direction in ("references", "both"):
            refs_raw = await s2.get_references(paper_id, limit=input.limit)
            result.references = [
                CitationPaper(
                    title=p.get("title"),
                    authors=p.get("authors", [])[:10],
                    year=p.get("year"),
                    doi=p.get("doi"),
                    arxiv_id=p.get("arxiv_id"),
                    venue=p.get("venue"),
                )
                for p in refs_raw
            ]

        return result

    except Exception as e:
        return CitationsResult(
            success=False,
            paper_id=input.identifier,
            error=str(e),
        )


# =============================================================================
# Helper Functions
# =============================================================================


def _parse_identifier(identifier: str) -> tuple[str | None, str | None]:
    """Parse identifier to determine if it's a DOI or title."""
    import re

    # Check for DOI pattern
    doi_pattern = r"^10\.\d{4,}/[^\s]+"
    if re.match(doi_pattern, identifier):
        return identifier, None

    # Check for arXiv pattern
    arxiv_pattern = r"^(arXiv:)?(\d{4}\.\d{4,}|[a-z-]+/\d{7})"
    if re.match(arxiv_pattern, identifier, re.IGNORECASE):
        return identifier, None

    # Assume it's a title
    return None, identifier


def _load_batch_file(path: Path) -> list[dict]:
    """Load batch file in various formats."""
    import json

    content = path.read_text(encoding="utf-8")

    # Try JSON
    if path.suffix == ".json":
        data = json.loads(content)
        if isinstance(data, list):
            return data
        return [data]

    # Try CSV
    if path.suffix == ".csv":
        import csv
        from io import StringIO
        reader = csv.DictReader(StringIO(content))
        return list(reader)

    # Plain text (one identifier per line)
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    items = []
    for line in lines:
        doi, title = _parse_identifier(line)
        items.append({"doi": doi, "title": title})
    return items


def _references_to_markdown(references: list[dict]) -> str:
    """Convert references to Markdown format."""
    lines = ["# Extracted References\n"]

    for i, ref in enumerate(references, 1):
        lines.append(f"## {i}. {ref.get('title', 'Unknown Title')}\n")

        if ref.get("authors"):
            lines.append(f"**Authors:** {ref['authors']}\n")
        if ref.get("year"):
            lines.append(f"**Year:** {ref['year']}\n")
        if ref.get("doi"):
            lines.append(f"**DOI:** [{ref['doi']}](https://doi.org/{ref['doi']})\n")
        if ref.get("arxiv_id"):
            lines.append(f"**arXiv:** [{ref['arxiv_id']}](https://arxiv.org/abs/{ref['arxiv_id']})\n")
        if ref.get("url"):
            lines.append(f"**URL:** {ref['url']}\n")

        lines.append("")

    return "\n".join(lines)


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
