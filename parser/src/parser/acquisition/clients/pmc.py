"""PubMed Central API client for biomedical literature."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

import httpx

from .base import BaseClient, RateLimiter


class PMCClient(BaseClient):
    """Client for PubMed Central APIs.

    Provides access to open access biomedical literature through:
    - ID conversion (DOI -> PMCID)
    - PDF URL discovery
    - Search by title
    """

    # New PMC API URLs (as of 2024)
    IDCONV_URL = "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/"
    OA_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"
    EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    # Direct PMC PDF URL patterns - try main.pdf first, then just pdf/
    PMC_PDF_URL = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/pdf/main.pdf"
    PMC_PDF_URL_ALT = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/pdf/"

    def __init__(
        self,
        api_key: str | None = None,
        email: str | None = None,
    ):
        """Initialize the PMC client.

        Args:
            api_key: NCBI API key for higher rate limits.
            email: Email for identification.
        """
        # NCBI allows 3/sec with API key, 10/sec without for registered tools
        rate = 3.0 if api_key else 1.0
        super().__init__(
            base_url=self.EUTILS_BASE,
            rate_limiter=RateLimiter(calls_per_second=rate)
        )
        self.api_key = api_key
        self.email = email

    async def doi_to_pmcid(self, doi: str) -> str | None:
        """Convert DOI to PMCID.

        Args:
            doi: The DOI to convert.

        Returns:
            PMCID or None if not found.
        """
        import asyncio
        import json
        import urllib.parse
        import urllib.request

        params = {
            "ids": doi,
            "format": "json",
            "tool": "parser",
            "email": self.email or "parser@example.com",
        }
        if self.api_key:
            params["api_key"] = self.api_key

        query = urllib.parse.urlencode(params)
        url = f"{self.IDCONV_URL}?{query}"

        def fetch():
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "parser/1.0"}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode())
                    records = data.get("records", [])
                    if records and "pmcid" in records[0]:
                        return records[0]["pmcid"]
            except Exception:
                pass
            return None

        # Run synchronous urllib in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, fetch)

    async def get_pdf_url(self, pmcid: str) -> str | None:
        """Get PDF URL for a PMCID.

        Args:
            pmcid: The PMCID to look up.

        Returns:
            PDF URL or None if not available.
        """
        # Normalize PMCID
        pmcid = f"PMC{pmcid}" if not pmcid.upper().startswith("PMC") else pmcid.upper()

        # First try the OA API for direct PDF link
        params: dict[str, Any] = {"id": pmcid, "format": "pdf"}

        try:
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                response = await client.get(self.OA_URL, params=params)
                response.raise_for_status()

                # Parse XML response for PDF link
                root = ET.fromstring(response.text)

                # Check for errors - if not OA, try direct PDF URL
                error = root.find(".//error")
                if error is None:
                    # Find PDF link
                    link = root.find(".//link[@format='pdf']")
                    if link is not None:
                        href = link.get("href")
                        # Convert FTP URLs to HTTPS if needed
                        if href and href.startswith("ftp://"):
                            href = href.replace("ftp://", "https://")
                        return href
        except Exception:
            pass
        
        # Try OA API without format to get tar.gz (will be handled by download method)
        try:
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                response = await client.get(self.OA_URL, params={"id": pmcid})
                response.raise_for_status()
                root = ET.fromstring(response.text)
                error = root.find(".//error")
                if error is None:
                    link = root.find(".//link[@format='tgz']")
                    if link is not None:
                        href = link.get("href")
                        if href:
                            # Mark as tar.gz for special handling
                            if href.startswith("ftp://"):
                                href = href.replace("ftp://", "https://")
                            return href
        except Exception:
            pass

        return None
    
    async def download_pdf(self, pmcid: str, output_path) -> bool:
        """Download PDF for a PMCID, handling tar.gz packages.
        
        Args:
            pmcid: The PMCID to download.
            output_path: Path to save the PDF.
            
        Returns:
            True if successful, False otherwise.
        """
        import io
        import tarfile
        from pathlib import Path
        
        url = await self.get_pdf_url(pmcid)
        if not url:
            return False
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
        }
        
        try:
            async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                content = response.content
                
                # Check if it's a tar.gz package
                if url.endswith('.tar.gz') or url.endswith('.tgz'):
                    # Extract PDF from tar.gz
                    with tarfile.open(fileobj=io.BytesIO(content), mode='r:gz') as tar:
                        for member in tar.getmembers():
                            if member.name.lower().endswith('.pdf'):
                                pdf_file = tar.extractfile(member)
                                if pdf_file:
                                    pdf_content = pdf_file.read()
                                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                                    Path(output_path).write_bytes(pdf_content)
                                    return True
                    return False
                
                # Direct PDF
                if content.startswith(b'%PDF') or 'pdf' in response.headers.get('content-type', '').lower():
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    Path(output_path).write_bytes(content)
                    return True
                    
        except Exception:
            pass
            
        return False

    async def search_by_title(
        self,
        title: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """Search PMC by title.

        Args:
            title: The title to search for.
            max_results: Maximum number of results.

        Returns:
            List of search results with PMCIDs.
        """
        params: dict[str, Any] = {
            "db": "pmc",
            "term": f'"{title}"[Title]',
            "retmax": str(max_results),
            "retmode": "json",
        }
        if self.api_key:
            params["api_key"] = self.api_key
        if self.email:
            params["email"] = self.email

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # First search for IDs
                search_url = f"{self.EUTILS_BASE}/esearch.fcgi"
                response = await client.get(search_url, params=params)
                response.raise_for_status()
                data = response.json()

                id_list = data.get("esearchresult", {}).get("idlist", [])
                if not id_list:
                    return []

                # Fetch summary for each ID
                summary_params: dict[str, Any] = {
                    "db": "pmc",
                    "id": ",".join(id_list),
                    "retmode": "json",
                }
                if self.api_key:
                    summary_params["api_key"] = self.api_key

                summary_url = f"{self.EUTILS_BASE}/esummary.fcgi"
                response = await client.get(summary_url, params=summary_params)
                response.raise_for_status()
                summary_data = response.json()

                results = []
                for uid in id_list:
                    item = summary_data.get("result", {}).get(uid, {})
                    if item:
                        results.append({
                            "pmcid": f"PMC{uid}",
                            "title": item.get("title", ""),
                            "doi": item.get("doi", ""),
                            "authors": item.get("authors", []),
                        })
                return results
        except Exception:
            return []

    async def get_metadata(self, pmcid: str) -> dict[str, Any] | None:
        """Get metadata for a PMCID.

        Args:
            pmcid: The PMCID to look up.

        Returns:
            Dict with metadata or None.
        """
        # Extract numeric ID
        numeric_id = pmcid.replace("PMC", "")

        params: dict[str, Any] = {
            "db": "pmc",
            "id": numeric_id,
            "retmode": "json",
        }
        if self.api_key:
            params["api_key"] = self.api_key

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{self.EUTILS_BASE}/esummary.fcgi"
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                item = data.get("result", {}).get(numeric_id, {})
                if item:
                    return {
                        "pmcid": pmcid,
                        "title": item.get("title", ""),
                        "doi": item.get("doi", ""),
                        "authors": [
                            a.get("name", "") for a in item.get("authors", [])
                        ],
                        "journal": item.get("fulljournalname", ""),
                        "year": item.get("pubdate", "")[:4] if item.get("pubdate") else None,
                    }
        except Exception:
            pass
        return None

    async def get_paper_metadata(self, identifier: str) -> dict[str, Any] | None:
        """Get metadata for a paper by identifier (DOI or PMCID).

        Args:
            identifier: DOI or PMCID.

        Returns:
            Paper metadata dict or None.
        """
        # Check if it's a PMCID
        if identifier.upper().startswith("PMC"):
            return await self.get_metadata(identifier)

        # Assume it's a DOI - convert to PMCID first
        pmcid = await self.doi_to_pmcid(identifier)
        if pmcid:
            metadata = await self.get_metadata(pmcid)
            if metadata:
                # Also get PDF URL
                pdf_url = await self.get_pdf_url(pmcid)
                if pdf_url:
                    metadata["pdf_url"] = pdf_url
                return metadata
        return None
