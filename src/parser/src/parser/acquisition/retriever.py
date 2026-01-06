"""Main paper retrieval orchestration.

Tries multiple sources in priority order to find and download PDFs.
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import httpx

from .config import Config
from .logger import RetrievalLogger
from .rate_limiter import RateLimiter


class RetrievalStatus(Enum):
    """Status of a retrieval attempt."""
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    ERROR = "error"
    SKIPPED = "skipped"
    FAILED = "failed"  # Alias for NOT_FOUND for CLI compatibility


@dataclass
class RetrievalResult:
    """Result of a paper retrieval attempt."""
    doi: str | None
    title: str
    status: RetrievalStatus
    source: str | None = None
    pdf_path: str | None = None
    error: str | None = None
    metadata: dict[str, Any] | None = None
    attempts: list[dict[str, Any]] | None = None  # History of attempted sources


class PaperRetriever:
    """Main orchestrator for paper PDF retrieval.

    Tries multiple sources in priority order to find PDFs.

    Example:
        >>> config = Config.load("config.yaml")
        >>> retriever = PaperRetriever(config)
        >>> result = await retriever.retrieve(doi="10.1234/example")
        >>> print(result.pdf_path)
    """

    def __init__(self, config: Config | None = None):
        """Initialize the paper retriever.

        Args:
            config: Configuration object (loads default if None)
        """
        self.config = config or Config.load()
        self.rate_limiter = RateLimiter(self.config.rate_limits)
        self.clients = self._init_clients()

    def _init_clients(self) -> dict[str, Any]:
        """Initialize all API clients with config-based rate limits."""
        from .clients import (
            ACLAnthologyClient,
            ArxivClient,
            BioRxivClient,
            CrossRefClient,
            FrontiersClient,
            OpenAlexClient,
            PMCClient,
            SemanticScholarClient,
            UnpaywallClient,
        )
        from .clients.base import RateLimiter as ClientRateLimiter

        # Get rate limits from config
        per_source_delays = self.config.rate_limits.get("per_source_delays", {})

        clients: dict[str, Any] = {
            "arxiv": ArxivClient(),
            "crossref": CrossRefClient(email=self.config.email),
            "semantic_scholar": SemanticScholarClient(
                api_key=self.config.api_keys.get("semantic_scholar")
            ),
            "pmc": PMCClient(
                api_key=self.config.api_keys.get("ncbi"),
                email=self.config.email,
            ),
            "biorxiv": BioRxivClient(use_selenium=True),
            "openalex": OpenAlexClient(email=self.config.email),
            "acl_anthology": ACLAnthologyClient(),
            "frontiers": FrontiersClient(use_selenium=True),
        }

        # Apply config rate limits to clients
        for name, client in clients.items():
            if hasattr(client, 'rate_limiter') and name in per_source_delays:
                delay = per_source_delays[name]
                # Convert delay (seconds) to calls_per_second
                calls_per_second = 1.0 / delay if delay > 0 else 10.0
                client.rate_limiter = ClientRateLimiter(calls_per_second=calls_per_second)

        # Unpaywall requires email
        if self.config.email:
            clients["unpaywall"] = UnpaywallClient(email=self.config.email)
            if "unpaywall" in per_source_delays:
                delay = per_source_delays["unpaywall"]
                calls_per_second = 1.0 / delay if delay > 0 else 10.0
                clients["unpaywall"].rate_limiter = ClientRateLimiter(calls_per_second=calls_per_second)

        # Initialize institutional client if configured
        inst_config = self.config.institutional
        if inst_config.get("enabled"):
            from .clients import InstitutionalAccessClient
            clients["institutional"] = InstitutionalAccessClient(
                proxy_url=inst_config.get("proxy_url"),
                vpn_enabled=inst_config.get("vpn_enabled", False),
                vpn_script=inst_config.get("vpn_script"),
                vpn_disconnect_script=inst_config.get("vpn_disconnect_script"),
                cookies_file=inst_config.get("cookies_file", ".institutional_cookies.pkl"),
                download_dir=self.config.download.get("output_dir", "./downloads"),
            )

        # Initialize web search client
        if self.config.is_source_enabled("web_search"):
            from .clients import WebSearchClient
            clients["web_search"] = WebSearchClient(enabled=True)

        # Initialize unofficial clients if disclaimer accepted
        if self.config.is_unofficial_enabled():
            unofficial_config = self.config.unofficial

            if self.config.is_source_enabled("scihub"):
                from .clients import ScihubClient
                unofficial_config.get("scihub", {})
                scihub_delay = per_source_delays.get("scihub", 5.0)
                clients["scihub"] = ScihubClient(
                    enabled=True,
                    timeout=60.0,
                    max_retries=self.config.batch.get("max_retries", 2),
                    rate_limit=scihub_delay,
                )

            if self.config.is_source_enabled("libgen"):
                from .clients import LibGenClient
                unofficial_config.get("libgen", {})
                libgen_delay = per_source_delays.get("libgen", 3.0)
                clients["libgen"] = LibGenClient(
                    enabled=True,
                    timeout=60.0,
                    max_retries=self.config.batch.get("max_retries", 2),
                    rate_limit=libgen_delay,
                )

        return clients

    async def retrieve(
        self,
        doi: str | None = None,
        title: str | None = None,
        arxiv_id: str | None = None,
        pdf_url: str | None = None,
        output_dir: Path | None = None,
        verbose: bool = True,
    ) -> RetrievalResult:
        """Retrieve PDF for a paper.

        Args:
            doi: Paper DOI
            title: Paper title
            arxiv_id: arXiv paper ID (e.g., "2301.12345")
            pdf_url: Direct PDF URL (tried first if provided)
            output_dir: Override output directory
            verbose: Show progress in console

        Returns:
            RetrievalResult with status and file path
        """
        if not doi and not title and not arxiv_id and not pdf_url:
            return RetrievalResult(
                doi=None,
                title="",
                status=RetrievalStatus.ERROR,
                error="Must provide DOI, title, arXiv ID, or PDF URL",
            )

        # Check if DOI is problematic (peer review, book chapter, etc.)
        if doi:
            from ..validation import classify_doi
            classification = classify_doi(doi)
            if classification.get("type") in ("review", "book_chapter"):
                warning = classification.get("warning", "Problematic DOI type")
                if verbose:
                    print(f"⚠ Skipping {classification['type']} DOI: {doi[:50]}...")
                    print(f"  Reason: {warning[:80]}")
                return RetrievalResult(
                    doi=doi,
                    title=title or "",
                    status=RetrievalStatus.SKIPPED,
                    error=warning,
                    metadata={"doi_type": classification["type"], "warning": warning},
                )

        # Setup output directory
        out_dir = Path(output_dir) if output_dir else Path(self.config.download.get("output_dir", "./downloads"))
        out_dir.mkdir(parents=True, exist_ok=True)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Create logger
        logger = RetrievalLogger(out_dir, doi, title, console_enabled=verbose)

        # Resolve metadata using universal title-first approach
        metadata = await self._resolve_metadata(doi, title, arxiv_id, pdf_url)
        resolved_doi = metadata.get("doi") if metadata else doi
        resolved_title = metadata.get("title") if metadata else title
        metadata.get("arxiv_id") if metadata else arxiv_id
        resolved_pdf_url = metadata.get("pdf_url") if metadata else pdf_url
        year = metadata.get("year") if metadata else None

        # Show header
        logger.header(resolved_doi, resolved_title, str(year) if year else None)

        # Generate output path
        output_path = self._get_output_path(metadata or {"doi": doi, "title": title}, out_dir)

        # Check if already downloaded
        if self.config.download.get("skip_existing") and output_path.exists():
            logger.final_result(True, "cached", str(output_path))
            return RetrievalResult(
                doi=resolved_doi,
                title=resolved_title or "",
                status=RetrievalStatus.SKIPPED,
                source="cached",
                pdf_path=str(output_path),
                metadata=metadata,
            )

        # Try direct PDF URL first if provided
        if resolved_pdf_url:
            logger.detail(f"Trying direct PDF URL: {resolved_pdf_url[:80]}...")
            if await self._download_pdf(resolved_pdf_url, output_path):
                logger.final_result(True, "direct_url", str(output_path))
                return RetrievalResult(
                    doi=resolved_doi,
                    title=resolved_title or title or "",
                    status=RetrievalStatus.SUCCESS,
                    source="direct_url",
                    pdf_path=str(output_path),
                    metadata=metadata,
                )
            else:
                logger.detail("Direct PDF URL download failed, trying other sources...")

        # Try sources in priority order
        sources = self.config.get_sorted_sources()
        total_sources = sum(1 for s in sources if self.config.is_source_enabled(s))

        source_index = 0
        for source_name in sources:
            if not self.config.is_source_enabled(source_name):
                continue

            # Skip unofficial sources if not enabled
            if source_name in ("scihub", "libgen") and not self.config.is_unofficial_enabled():
                continue

            source_index += 1
            logger.source_start(source_index, total_sources, source_name)

            await self.rate_limiter.wait(source_name)

            result, reason = await self._try_source(
                source_name,
                resolved_doi,
                resolved_title or title or "",
                metadata or {},
                output_path,
                logger,
            )

            if result and result.status == RetrievalStatus.SUCCESS:
                logger.source_result(source_index, total_sources, source_name, True, reason, result.pdf_path)
                logger.final_result(True, source_name, result.pdf_path)
                result.metadata = metadata
                return result
            else:
                logger.source_result(source_index, total_sources, source_name, False, reason)

        logger.final_result(False)
        return RetrievalResult(
            doi=resolved_doi,
            title=resolved_title or title or "",
            status=RetrievalStatus.NOT_FOUND,
            error="PDF not found in any source",
            metadata=metadata,
        )

    async def _resolve_metadata(
        self,
        doi: str | None = None,
        title: str | None = None,
        arxiv_id: str | None = None,
        pdf_url: str | None = None,
    ) -> dict[str, Any] | None:
        """Resolve full metadata from title, DOI, arXiv ID, or PDF URL.

        Universal priority order (title-first for best DOI discovery):
        1. TITLE SEARCH (universal - works for any paper, finds DOI)
           - CrossRef title search (peer-reviewed)
           - Semantic Scholar title search (broad coverage)
        2. DOI LOOKUP (if provided or found via title search)
           - CrossRef by DOI
           - Semantic Scholar by DOI
           - OpenAlex by DOI
        3. ARXIV ID LOOKUP (if provided, no DOI found)
           - Semantic Scholar by arXiv ID
           - arXiv direct search
        4. PDF URL (stored in metadata for direct download attempts)
        """
        from ..validation import classify_doi

        # Extract arXiv ID from various formats
        if doi:
            if doi.startswith("arXiv:"):
                arxiv_id = doi[6:]  # Remove "arXiv:" prefix
                doi = None
            elif doi.startswith("10.48550/arXiv."):
                # arXiv DOI format: 10.48550/arXiv.YYMM.NNNNN
                arxiv_id = doi.replace("10.48550/arXiv.", "")
                # Keep the DOI too for CrossRef lookup

        # Also extract arXiv ID from PDF URL if present
        if pdf_url and not arxiv_id:
            arxiv_match = re.search(r"arxiv\.org/(?:abs|pdf)/([\d.]+)", pdf_url)
            if arxiv_match:
                arxiv_id = arxiv_match.group(1)

        # ============================================================
        # PHASE 1: TITLE SEARCH (Universal - finds DOI for any paper)
        # ============================================================
        if title:
            # 1a. Try Semantic Scholar title search FIRST (better coverage, less rate limited)
            s2 = self.clients.get("semantic_scholar")
            if s2:
                try:
                    await self.rate_limiter.wait("semantic_scholar")
                    results = await s2.search(title, limit=5)
                    for result in results:
                        if result and result.get("year") and self._titles_match(title, result.get("title", ""), threshold=0.8):
                            found_doi = result.get("doi")
                            found_arxiv = result.get("arxiv_id")
                            return {
                                "doi": found_doi,
                                "title": result.get("title"),
                                "authors": result.get("authors", []),
                                "year": result.get("year"),
                                "venue": result.get("venue"),
                                "arxiv_id": found_arxiv,
                                "pdf_url": pdf_url,  # Preserve original PDF URL
                            }
                except Exception:
                    pass

            # 1b. Try CrossRef title search (peer-reviewed papers)
            crossref = self.clients.get("crossref")
            if crossref:
                try:
                    await self.rate_limiter.wait("crossref")
                    results = await crossref.search(title, limit=5)
                    for result in results:
                        result_doi = result.get("doi")
                        # Validate DOI is not a book chapter or review
                        if result_doi:
                            classification = classify_doi(result_doi)
                            if classification.get("type") in ("review", "book_chapter"):
                                continue  # Skip this result
                        # Check title similarity with higher threshold
                        if result and result.get("year") and result.get("authors") and self._titles_match(title, result.get("title", ""), threshold=0.8):
                            result["pdf_url"] = pdf_url  # Preserve original PDF URL
                            return result
                except Exception:
                    pass

        # ============================================================
        # PHASE 2: DOI LOOKUP (if DOI was provided directly)
        # ============================================================
        if doi and not doi.startswith("10.48550/arXiv"):
            # 2a. Try CrossRef by DOI (most authoritative for peer-reviewed)
            crossref = self.clients.get("crossref")
            if crossref:
                try:
                    await self.rate_limiter.wait("crossref")
                    metadata = await crossref.get_paper_metadata(doi)
                    if metadata and metadata.get("year") and metadata.get("authors"):
                        metadata["pdf_url"] = pdf_url
                        return metadata
                except Exception:
                    pass

            # 2b. Try Semantic Scholar by DOI
            s2 = self.clients.get("semantic_scholar")
            if s2:
                try:
                    await self.rate_limiter.wait("semantic_scholar")
                    result = await s2.get_paper_metadata(f"DOI:{doi}")
                    if result and result.get("year") and result.get("authors"):
                        return {
                            "doi": result.get("doi") or doi,
                            "title": result.get("title"),
                            "authors": result.get("authors", []),
                            "year": result.get("year"),
                            "venue": result.get("venue"),
                            "arxiv_id": result.get("arxiv_id"),
                            "pdf_url": pdf_url,
                        }
                except Exception:
                    pass

            # 2c. Try OpenAlex by DOI (broad coverage)
            openalex = self.clients.get("openalex")
            if openalex:
                try:
                    await self.rate_limiter.wait("openalex")
                    result = await openalex.get_paper_metadata(doi)
                    if result:
                        authorships = result.get("authorships", [])
                        authors = []
                        for authorship in authorships[:3]:
                            author = authorship.get("author", {})
                            name = author.get("display_name")
                            if name:
                                authors.append({"name": name})

                        pub_year = result.get("publication_year")
                        if pub_year and authors:
                            return {
                                "doi": result.get("doi") or doi,
                                "title": result.get("title"),
                                "authors": authors,
                                "year": pub_year,
                                "venue": result.get("host_venue", {}).get("display_name"),
                                "pdf_url": pdf_url,
                            }
                except Exception:
                    pass

        # ============================================================
        # PHASE 3: ARXIV ID LOOKUP (if arXiv ID provided, no DOI found)
        # ============================================================
        if arxiv_id:
            # 3a. Try Semantic Scholar by arXiv ID
            s2 = self.clients.get("semantic_scholar")
            if s2:
                try:
                    await self.rate_limiter.wait("semantic_scholar")
                    result = await s2.get_paper_metadata(f"ARXIV:{arxiv_id}")
                    if result and result.get("year") and result.get("authors"):
                        return {
                            "doi": result.get("doi"),
                            "title": result.get("title"),
                            "authors": result.get("authors", []),
                            "year": result.get("year"),
                            "venue": result.get("venue"),
                            "arxiv_id": result.get("arxiv_id") or arxiv_id,
                            "pdf_url": pdf_url or f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                        }
                except Exception:
                    pass

            # 3b. Try arXiv direct API
            arxiv_client = self.clients.get("arxiv")
            if arxiv_client:
                try:
                    await self.rate_limiter.wait("arxiv")
                    # Search by arXiv ID directly
                    results = await arxiv_client.search(arxiv_id, limit=1)
                    for result in results:
                        found_arxiv_id = result.get("arxiv_id")
                        if found_arxiv_id:
                            return {
                                "doi": f"10.48550/arXiv.{found_arxiv_id.split('v')[0]}",
                                "title": result.get("title"),
                                "authors": result.get("authors", []),
                                "year": result.get("year"),
                                "venue": "arXiv (preprint)",
                                "arxiv_id": found_arxiv_id,
                                "is_preprint": True,
                                "pdf_url": pdf_url or f"https://arxiv.org/pdf/{found_arxiv_id}.pdf",
                            }
                except Exception:
                    pass

        # ============================================================
        # PHASE 4: TITLE-ONLY ARXIV SEARCH (fallback for preprints)
        # ============================================================
        if title and not doi:
            arxiv_client = self.clients.get("arxiv")
            if arxiv_client:
                try:
                    await self.rate_limiter.wait("arxiv")
                    quoted_title = f'"{title}"'
                    results = await arxiv_client.search(quoted_title, limit=5)
                    for result in results:
                        found_title = result.get("title", "")
                        if result.get("arxiv_id") and self._titles_match(title, found_title, threshold=0.8):
                            found_arxiv_id = result["arxiv_id"]
                            return {
                                "doi": f"10.48550/arXiv.{found_arxiv_id.split('v')[0]}",
                                "title": found_title,
                                "authors": result.get("authors", []),
                                "year": result.get("year"),
                                "venue": "arXiv (preprint)",
                                "arxiv_id": found_arxiv_id,
                                "is_preprint": True,
                                "pdf_url": pdf_url or f"https://arxiv.org/pdf/{found_arxiv_id}.pdf",
                            }
                except Exception:
                    pass

        # No metadata found, return minimal info with any provided identifiers
        return {"doi": doi, "title": title, "arxiv_id": arxiv_id, "pdf_url": pdf_url}

    def _get_output_path(self, metadata: dict[str, Any], output_dir: Path) -> Path:
        """Generate output file path from metadata using config filename format."""
        # Get components
        authors = metadata.get("authors", [])
        first_author = ""
        if authors:
            if isinstance(authors[0], dict):
                first_author = authors[0].get("family", "") or authors[0].get("name", "").split()[-1]
            else:
                first_author = str(authors[0]).split()[-1]

        # Clean first_author - remove any remaining whitespace/special chars
        if first_author:
            first_author = re.sub(r"[^\w-]", "", first_author)

        # Fallback to DOI-based author if missing
        if not first_author and metadata.get("doi"):
            # Extract something from DOI as fallback
            doi_parts = metadata["doi"].split("/")
            if len(doi_parts) > 1:
                first_author = doi_parts[1].split(".")[0][:10]  # Use first part of DOI suffix

        year = str(metadata.get("year", "")) if metadata.get("year") else ""
        title = metadata.get("title", "") or ""

        # Clean title and create short version
        max_len = self.config.download.get("max_title_length", 50)
        if title:
            # Remove special characters
            title_clean = re.sub(r"[^\w\s-]", "", title)
            # Split into words and limit
            words = title_clean.split()[:7]  # Max 7 words
            title_short = "_".join(words)[:max_len].strip()
        else:
            title_short = ""

        # Get filename format from config
        filename_format = self.config.download.get(
            "filename_format",
            "{first_author}_{year}_{title_short}.pdf"
        )

        # Build filename using format string
        try:
            filename = filename_format.format(
                first_author=first_author or "Unknown",
                year=year or "XXXX",
                title_short=title_short or "paper",
                title=title or "paper",
                doi=metadata.get("doi", "").replace("/", "_").replace(".", "_") if metadata.get("doi") else "unknown",
            )
        except KeyError:
            # Fallback if format string has unknown placeholders
            filename = "paper.pdf"

        # Clean up filename - replace spaces and multiple underscores
        filename = filename.replace(" ", "_")
        filename = re.sub(r"_+", "_", filename)  # Remove multiple underscores
        filename = filename.strip("_")  # Remove leading/trailing underscores

        # Ensure filename is not empty or just underscores/extension
        if filename in ("_.pdf", ".pdf", "pdf") or not filename:
            # Use DOI if available
            if metadata.get("doi"):
                filename = metadata["doi"].replace("/", "_").replace(".", "_") + ".pdf"
            else:
                # Last resort: use timestamp
                import time
                filename = f"paper_{int(time.time())}.pdf"

        # Ensure .pdf extension
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        # Check if we should create subfolders (one per paper)
        if self.config.download.get("create_subfolders", False):
            # Create subfolder named after the paper (without .pdf extension)
            subfolder_name = filename.rsplit(".", 1)[0]  # Remove .pdf
            subfolder = output_dir / subfolder_name
            subfolder.mkdir(parents=True, exist_ok=True)
            return subfolder / filename

        return output_dir / filename

    async def _try_source(
        self,
        source: str,
        doi: str | None,
        title: str,
        metadata: dict[str, Any],
        output_path: Path,
        logger: RetrievalLogger,
    ) -> tuple[RetrievalResult | None, str]:
        """Try to retrieve PDF from a specific source."""
        client = self.clients.get(source)
        if not client:
            return None, "client not configured"

        try:
            if source == "unpaywall":
                return await self._try_unpaywall(client, doi, title, output_path, logger)

            elif source == "arxiv":
                return await self._try_arxiv(client, doi, title, output_path, logger)

            elif source == "pmc":
                return await self._try_pmc(client, doi, title, output_path, logger)

            elif source == "biorxiv":
                return await self._try_biorxiv(client, doi, title, output_path, logger)

            elif source == "semantic_scholar":
                return await self._try_semantic_scholar(client, doi, title, output_path, logger)

            elif source == "acl_anthology":
                return await self._try_acl_anthology(client, doi, title, output_path, logger)

            elif source == "frontiers":
                return await self._try_frontiers(client, doi, title, output_path, logger)

            elif source == "openalex":
                return await self._try_openalex(client, doi, title, output_path, logger)

            elif source == "institutional":
                return await self._try_institutional(client, doi, title, output_path, logger)

            elif source == "web_search":
                return await self._try_web_search(client, doi, title, metadata, output_path, logger)

            elif source == "scihub":
                return await self._try_scihub(client, doi, title, output_path, logger)

            elif source == "libgen":
                return await self._try_libgen(client, doi, title, output_path, logger)

        except Exception as e:
            logger.error(source, str(e))
            return None, f"error: {e}"

        return None, "unknown source"

    async def _try_unpaywall(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try Unpaywall source."""
        if not doi:
            return None, "no DOI provided"

        logger.detail(f"Checking OA status for {doi}")
        pdf_url = await client.get_pdf_url(doi)

        if not pdf_url:
            return None, "no OA version found"

        logger.detail(f"Found PDF: {pdf_url}")
        if await self._download_pdf(pdf_url, output_path):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="unpaywall", pdf_path=str(output_path),
            ), "downloaded"
        return None, "PDF download failed"

    async def _try_arxiv(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try arXiv source.

        Order of attempts:
        1. arXiv ID (if provided in DOI like 10.48550/arXiv.XXXX.XXXXX)
        2. arXiv URL (if title contains arxiv.org URL)
        3. Title search (search arXiv by title with strict matching)
        """
        arxiv_id = None

        # 1. Extract arXiv ID from DOI (e.g., 10.48550/arXiv.1706.03762)
        if doi and "arxiv" in doi.lower():
            logger.detail(f"arXiv DOI detected: {doi}")
            match = re.search(r"arxiv\.(\d+\.\d+)", doi.lower())
            if match:
                arxiv_id = match.group(1)

        # 2. Check if title contains arXiv URL (e.g., "https://arxiv.org/abs/1706.03762")
        if not arxiv_id and title:
            url_match = re.search(r"arxiv\.org/(?:abs|pdf)/([\d.]+)", title)
            if url_match:
                arxiv_id = url_match.group(1)
                logger.detail(f"arXiv URL detected in title: {arxiv_id}")

        # Try direct download if we have an arXiv ID
        if arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            logger.detail(f"Trying arXiv ID {arxiv_id}: {pdf_url}")
            if await self._download_pdf(pdf_url, output_path):
                return RetrievalResult(
                    doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                    source="arxiv", pdf_path=str(output_path),
                ), "downloaded via arXiv ID"
            else:
                logger.detail(f"Direct download failed for arXiv ID {arxiv_id}")

        # 3. Search by title using arXiv search API
        if title:
            logger.detail(f"Searching arXiv by title: {title[:50]}...")
            # Use quoted search for better exact matching
            quoted_title = f'"{title}"'
            results = await client.search(quoted_title, limit=5)
            for metadata in results:
                found_arxiv_id = metadata.get("arxiv_id")
                found_title = metadata.get("title", "")
                if found_arxiv_id and self._titles_match(title, found_title, threshold=0.7):
                    pdf_url = f"https://arxiv.org/pdf/{found_arxiv_id}.pdf"
                    logger.detail(f"Title match found ('{found_title[:40]}...'), PDF: {pdf_url}")
                    if await self._download_pdf(pdf_url, output_path):
                        return RetrievalResult(
                            doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                            source="arxiv", pdf_path=str(output_path),
                        ), "downloaded via title search"

        return None, "not found on arXiv"

    async def _try_pmc(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try PMC source."""
        if not doi:
            return None, "no DOI provided"

        logger.detail(f"Looking up PMC ID for {doi}")
        pmcid = await client.doi_to_pmcid(doi)

        if not pmcid:
            return None, "no PMC ID for this DOI"

        logger.detail(f"Found PMC ID: {pmcid}")

        # Use PMC client's download_pdf method which handles tar.gz packages
        if await client.download_pdf(pmcid, output_path):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="pmc", pdf_path=str(output_path),
            ), "downloaded"
        return None, "PDF download failed"

    async def _try_biorxiv(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try bioRxiv source with Selenium fallback for bot protection."""
        if not doi:
            return None, "no DOI provided"
        if not doi.startswith("10.1101"):
            return None, "not a bioRxiv DOI"

        logger.detail(f"Checking bioRxiv for {doi}")

        # Use the client's download_pdf method which has Selenium fallback
        if await client.download_pdf(doi, output_path):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="biorxiv", pdf_path=str(output_path),
            ), "downloaded"
        return None, "PDF download failed (bot protection)"

    async def _try_frontiers(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try Frontiers source with Selenium for bot protection.

        Frontiers is a Gold OA publisher but uses CloudFlare protection.
        """
        if not doi:
            return None, "no DOI provided"

        if not client.is_frontiers_doi(doi):
            return None, "not a Frontiers DOI"

        logger.detail(f"Frontiers DOI detected: {doi}")
        result = await client.download_by_doi(doi, output_path)

        if result and result.get("pdf_path"):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="frontiers", pdf_path=result["pdf_path"],
            ), "downloaded"
        return None, "PDF download failed (bot protection)"

    async def _try_semantic_scholar(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try Semantic Scholar source."""
        result = None

        if doi:
            # Validate the DOI before using it
            is_valid, rejection_reason = self._validate_found_doi(title, doi)
            if not is_valid:
                logger.detail(f"DOI validation failed: {rejection_reason}")
                doi = None  # Don't use this DOI, fall through to title search
            else:
                logger.detail(f"Looking up paper by DOI: {doi}")
                result = await client.get_paper_metadata(f"DOI:{doi}")

        if not result or not result.get("pdf_url"):
            logger.detail(f"Searching by title: {title[:50]}...")
            results = await client.search(title, limit=5)
            for r in results:
                found_doi = r.get("doi")
                found_title = r.get("title", "")

                # Validate title match
                if not self._titles_match(title, found_title):
                    continue

                # Validate DOI if present
                if found_doi:
                    is_valid, rejection_reason = self._validate_found_doi(title, found_doi, found_title, r.get("abstract", ""))
                    if not is_valid:
                        logger.detail(f"Skipping DOI {found_doi}: {rejection_reason}")
                        continue

                if r.get("pdf_url"):
                    result = r
                    break

        if not result or not result.get("pdf_url"):
            return None, "no open access PDF"

        pdf_url = result["pdf_url"]
        logger.detail(f"PDF URL: {pdf_url}")

        if await self._download_pdf(pdf_url, output_path):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="semantic_scholar", pdf_path=str(output_path),
            ), "downloaded"
        return None, "PDF download failed"

    async def _try_acl_anthology(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try ACL Anthology source for NLP papers.

        ACL Anthology hosts papers from ACL, EMNLP, NAACL, etc.
        All papers are freely available.
        """
        if not doi:
            return None, "no DOI provided"

        # Check if it's an ACL DOI
        if not client.is_acl_doi(doi):
            return None, "not an ACL DOI"

        logger.detail(f"ACL Anthology DOI detected: {doi}")
        result = await client.download_by_doi(doi, output_path)

        if result and result.get("pdf_path"):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="acl_anthology", pdf_path=result["pdf_path"],
            ), "downloaded"
        return None, "PDF download failed"

    async def _try_openalex(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try OpenAlex source."""
        result = None

        if doi:
            # Validate the DOI before using it
            is_valid, rejection_reason = self._validate_found_doi(title, doi)
            if not is_valid:
                logger.detail(f"DOI validation failed: {rejection_reason}")
                doi = None  # Fall through to title search
            else:
                logger.detail(f"Looking up work by DOI: {doi}")
                result = await client.get_paper_metadata(doi)

        if not result:
            logger.detail(f"Searching by title: {title[:50]}...")
            results = await client.search(title, limit=5)
            for r in results:
                found_title = r.get("title", "")
                found_doi = r.get("doi")

                # Validate title match
                if not self._titles_match(title, found_title):
                    continue

                # Validate DOI if present
                if found_doi:
                    is_valid, rejection_reason = self._validate_found_doi(title, found_doi, found_title)
                    if not is_valid:
                        logger.detail(f"Skipping result: {rejection_reason}")
                        continue

                result = r
                break

        if not result:
            return None, "work not found"

        # Check for open access PDF - try pdf_url first, then open_access.oa_url
        oa_url = result.get("pdf_url") or result.get("open_access", {}).get("oa_url")
        if not oa_url:
            return None, "no OA URL"

        logger.detail(f"OA URL: {oa_url}")

        # Extract direct PDF URL from landing pages
        pdf_url = await self._extract_pdf_url_from_landing_page(oa_url, logger)
        if not pdf_url:
            pdf_url = oa_url  # Try original URL as fallback

        if await self._download_pdf(pdf_url, output_path):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="openalex", pdf_path=str(output_path),
            ), "downloaded"
        return None, "PDF download failed"

    async def _extract_pdf_url_from_landing_page(self, url: str, logger) -> str | None:
        """Extract direct PDF URL from repository landing pages.

        Handles common repository patterns:
        - HAL (French national archive)
        - Institutional repositories
        - Other landing pages with PDF links
        """
        # HAL (hal.science, hal.archives-ouvertes.fr)
        if "hal.science" in url or "hal.archives-ouvertes.fr" in url:
            # HAL pattern: append /document or /file to get PDF
            base_url = url.rstrip("/")
            pdf_url = f"{base_url}/document"
            logger.detail(f"HAL repository detected, trying: {pdf_url}")
            return pdf_url

        # For other landing pages, try to parse HTML for PDF links
        try:
            import httpx
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as http_client:
                response = await http_client.get(url)
                if response.status_code == 200:
                    html = response.text
                    # Look for common PDF link patterns
                    import re

                    # Pattern 1: Direct PDF link in href
                    pdf_link_patterns = [
                        r'href=["\']([^"\']+\.pdf)["\']',
                        r'href=["\']([^"\']+/download[^"\']*)["\']',
                        r'href=["\']([^"\']+/pdf[^"\']*)["\']',
                    ]

                    for pattern in pdf_link_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        if matches:
                            pdf_path = matches[0]
                            # Make absolute URL if relative
                            if pdf_path.startswith('/'):
                                from urllib.parse import urlparse
                                parsed = urlparse(url)
                                pdf_url = f"{parsed.scheme}://{parsed.netloc}{pdf_path}"
                            elif not pdf_path.startswith('http'):
                                pdf_url = url.rsplit('/', 1)[0] + '/' + pdf_path
                            else:
                                pdf_url = pdf_path
                            logger.detail(f"Extracted PDF URL from landing page: {pdf_url}")
                            return pdf_url
        except Exception as e:
            logger.detail(f"Could not extract PDF from landing page: {e}")

        return None

    async def _try_institutional(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try institutional access."""
        if not doi:
            return None, "no DOI provided"
        if not client.is_authenticated():
            return None, "not authenticated"

        logger.detail(f"Accessing via EZProxy: {doi}")
        if await client.download_pdf(doi, output_path):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="institutional", pdf_path=str(output_path),
            ), "downloaded"
        return None, "institutional download failed"

    async def _try_web_search(self, client, doi, title, metadata, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try web search."""
        authors = metadata.get("authors", [])
        author_names = [a.get("family", "") or a.get("name", "") for a in authors if isinstance(a, dict)]

        logger.detail(f"Web searching for: {title[:50]}...")
        result = await client.search_for_pdf(title=title, doi=doi, authors=author_names)

        if not result or not result.get("pdf_url"):
            return None, "no PDF found via web search"

        logger.detail(f"Found: {result['pdf_url']}")
        if await self._download_pdf(result["pdf_url"], output_path):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="web_search", pdf_path=str(output_path),
            ), "downloaded"
        return None, "PDF download failed"

    async def _try_scihub(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try Sci-Hub (unofficial).

        Lookup priority: title -> DOI (title first tends to have better hit rate)
        """
        logger.detail("Trying Sci-Hub mirrors...")
        result = None

        # Priority: title first (better hit rate for some papers)
        lookup_priority = self.config.download.get("lookup_priority", ["title", "doi"])

        for method in lookup_priority:
            if result:
                break
            if method == "title" and title:
                logger.detail(f"Trying by title: {title[:40]}...")
                result = await client.download_by_title(title, output_path)
            elif method == "doi" and doi:
                logger.detail(f"Trying by DOI: {doi}")
                result = await client.download_by_doi(doi, output_path)

        if result and result.get("pdf_path"):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="scihub", pdf_path=result["pdf_path"],
            ), "downloaded"
        return None, "not available or bot protection"

    async def _try_libgen(self, client, doi, title, output_path, logger) -> tuple[RetrievalResult | None, str]:
        """Try LibGen (unofficial).

        Lookup priority: title -> DOI (title first tends to have better hit rate)
        """
        logger.detail("Trying LibGen mirrors...")
        result = None

        # Priority: title first (better hit rate for some papers)
        lookup_priority = self.config.download.get("lookup_priority", ["title", "doi"])

        for method in lookup_priority:
            if result:
                break
            if method == "title" and title:
                logger.detail(f"Trying by title: {title[:40]}...")
                result = await client.download_by_title(title, output_path)
            elif method == "doi" and doi:
                logger.detail(f"Trying by DOI: {doi}")
                result = await client.download_by_doi(doi, output_path)

        if result and result.get("pdf_path"):
            return RetrievalResult(
                doi=doi, title=title, status=RetrievalStatus.SUCCESS,
                source="libgen", pdf_path=result["pdf_path"],
            ), "downloaded"
        return None, "not available or connection failed"

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Normalize a title for comparison."""
        normalized = re.sub(r"[^\w\s]", "", title.lower())
        return " ".join(normalized.split())

    def _titles_match(self, title1: str, title2: str, threshold: float = 0.6) -> bool:
        """Check if two titles are similar enough.

        Uses two methods:
        1. Substring match: If one title contains the other (for truncated titles)
           Only matches if shorter is at least 60% of longer length
        2. Word overlap: Jaccard similarity of words

        Args:
            title1: First title (usually the query)
            title2: Second title (usually the found result)
            threshold: Minimum similarity score (0.0 to 1.0), default 0.6
        """
        norm1 = self._normalize_title(title1)
        norm2 = self._normalize_title(title2)

        # Check for substring match (handles truncated titles)
        # Only allow if shorter title is at least 60% of the longer title length
        # This prevents "The NeXus data format" from matching
        # "The application of the NeXus data format to ISIS muon data"
        if norm1 in norm2 or norm2 in norm1:
            shorter_len = min(len(norm1), len(norm2))
            longer_len = max(len(norm1), len(norm2))
            if shorter_len >= longer_len * 0.6:
                return True

        words1 = set(norm1.split())
        words2 = set(norm2.split())

        if not words1 or not words2:
            return False

        # Check if all words from the shorter title are in the longer title
        # This handles cases like partial titles, but only if word count is similar
        # (to prevent matching e.g. "data format" with "new data format system for X")
        shorter, longer = (words1, words2) if len(words1) <= len(words2) else (words2, words1)
        if shorter.issubset(longer) and len(shorter) >= len(longer) * 0.6:
            return True

        # Fall back to Jaccard similarity
        common = len(words1 & words2)
        total = len(words1 | words2)
        return common / total >= threshold if total > 0 else False

    def _validate_found_doi(self, expected_title: str, found_doi: str, found_title: str = "", found_abstract: str = "") -> tuple[bool, str | None]:
        """Validate that a DOI found during search is appropriate.

        This catches cases like:
        - Peer review DOIs instead of paper DOIs
        - Book chapter DOIs when the original paper is elsewhere
        - False positive title matches (e.g., "llama" animal vs "LLaMA" AI model)

        Args:
            expected_title: The title we're looking for
            found_doi: The DOI that was found
            found_title: The title from the DOI metadata
            found_abstract: Optional abstract text

        Returns:
            Tuple of (is_valid, rejection_reason)
        """
        from ..validation import classify_doi, detect_title_context_mismatch

        # Check DOI classification
        classification = classify_doi(found_doi)
        if classification.get("type") in ("review", "book_chapter", "dataset"):
            return False, f"Rejected: {classification.get('warning', 'problematic DOI type')}"

        # Check title context mismatch (catches "llama" animal vs "LLaMA" AI)
        if found_title:
            is_mismatch, reason = detect_title_context_mismatch(
                expected_title, found_title, found_abstract
            )
            if is_mismatch:
                return False, f"Rejected: {reason}"

        return True, None

    async def _download_pdf(self, url: str, output_path: Path) -> bool:
        """Download PDF from URL."""
        # Use browser-like headers to avoid blocks
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/pdf,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": url.split("/content/")[0] + "/" if "/content/" in url else url,
        }

        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()

                content = response.content
                content_type = response.headers.get("content-type", "")

                # Verify it's a PDF
                if "pdf" not in content_type.lower() and not content.startswith(b"%PDF"):
                    return False

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(content)
                return True

        except Exception:
            return False

    async def retrieve_batch(
        self,
        papers: list[dict[str, Any]],
        output_dir: Path | None = None,
        verbose: bool = True,
        save_progress: bool = True,
        max_concurrent: int = 1,
    ) -> list[RetrievalResult]:
        """Retrieve PDFs for multiple papers.

        Args:
            papers: List of dicts with keys: 'title', 'doi', 'arxiv_id', 'pdf_url'
                   - title: Paper title (used for universal search)
                   - doi: Paper DOI (optional)
                   - arxiv_id: arXiv paper ID (optional, e.g., "2301.12345")
                   - pdf_url: Direct PDF URL (optional, tried first if provided)
            output_dir: Override output directory
            verbose: Show progress
            save_progress: Save progress to file for resume
            max_concurrent: Maximum concurrent downloads (default 1 for rate limiting)

        Returns:
            List of RetrievalResult objects
        """
        out_dir = Path(output_dir) if output_dir else Path(self.config.download.get("output_dir", "./downloads"))
        out_dir.mkdir(parents=True, exist_ok=True)

        progress_file = out_dir / self.config.batch.get("progress_file", ".retrieval_progress.json")
        completed: set[str] = set()

        # Load existing progress
        if save_progress and progress_file.exists():
            try:
                with open(progress_file) as f:
                    progress_data = json.load(f)
                    completed = set(progress_data.get("completed", []))
                if verbose:
                    print(f"Resuming from {len(completed)} completed papers")
            except Exception:
                pass

        results = []
        total = len(papers)

        # Use semaphore for concurrency control
        semaphore = asyncio.Semaphore(max_concurrent)

        async def retrieve_one(idx: int, paper: dict) -> tuple[int, RetrievalResult]:
            async with semaphore:
                doi = paper.get("doi")
                title = paper.get("title", "")
                arxiv_id = paper.get("arxiv_id")
                pdf_url = paper.get("pdf_url")
                identifier = doi or title or arxiv_id or pdf_url

                # Skip if already completed
                if identifier in completed:
                    if verbose:
                        print(f"[{idx}/{total}] Skipping (already done): {identifier[:50]}")
                    return idx, RetrievalResult(
                        doi=doi, title=title or "",
                        status=RetrievalStatus.SKIPPED,
                        pdf_path=None,
                    )

                if verbose:
                    print(f"\n[{idx}/{total}] Processing: {identifier[:60]}...")

                result = await self.retrieve(
                    doi=doi,
                    title=title,
                    arxiv_id=arxiv_id,
                    pdf_url=pdf_url,
                    output_dir=out_dir,
                    verbose=verbose,
                )

                # Save progress
                if save_progress and result.status in (RetrievalStatus.SUCCESS, RetrievalStatus.SKIPPED):
                    completed.add(identifier)
                    try:
                        with open(progress_file, "w") as f:
                            json.dump({"completed": list(completed)}, f)
                    except Exception:
                        pass

                return idx, result

        if max_concurrent > 1:
            # Concurrent execution
            tasks = [retrieve_one(i, paper) for i, paper in enumerate(papers, 1)]
            task_results = await asyncio.gather(*tasks)
            # Sort by original index
            task_results.sort(key=lambda x: x[0])
            results = [r for _, r in task_results]
        else:
            # Sequential execution (original behavior)
            for i, paper in enumerate(papers, 1):
                _, result = await retrieve_one(i, paper)
                results.append(result)
                # Rate limit between papers
                await asyncio.sleep(self.config.rate_limits.get("global_delay", 1.0))

        return results
