"""ACL Anthology client for downloading NLP papers.

ACL Anthology (https://aclanthology.org/) is an open-access archive
of papers from the Association for Computational Linguistics and 
related organizations (EMNLP, NAACL, CoNLL, etc.).

All papers are freely available - no authentication needed.
"""

from __future__ import annotations

import asyncio
import re
import time
from pathlib import Path
from typing import Any

import httpx


class ACLAnthologyClient:
    """Client for downloading papers from ACL Anthology.
    
    ACL Anthology hosts papers from:
    - ACL (Association for Computational Linguistics)
    - EMNLP (Empirical Methods in NLP)
    - NAACL (North American ACL)
    - EACL (European ACL)
    - CoNLL (Computational Natural Language Learning)
    - And many other NLP venues
    
    DOI format: 10.18653/v1/{anthology_id}
    Example: 10.18653/v1/N19-1423 (BERT paper)
    """
    
    BASE_URL = "https://aclanthology.org"
    DOI_PREFIX = "10.18653/v1/"
    
    def __init__(
        self,
        enabled: bool = True,
        timeout: float = 30.0,
        rate_limit: float = 1.0,
    ):
        """Initialize the ACL Anthology client.
        
        Args:
            enabled: Whether the client is enabled
            timeout: Request timeout in seconds
            rate_limit: Seconds between requests
        """
        self.enabled = enabled
        self.timeout = timeout
        self.rate_limit = rate_limit
        self._last_request: float = 0.0
    
    async def _rate_limit_wait(self) -> None:
        """Wait to respect rate limits."""
        now = time.time()
        elapsed = now - self._last_request
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self._last_request = time.time()
    
    def _extract_anthology_id(self, doi: str) -> str | None:
        """Extract ACL Anthology ID from DOI.
        
        Args:
            doi: DOI like "10.18653/v1/N19-1423"
            
        Returns:
            Anthology ID like "N19-1423" or None
        """
        if not doi:
            return None
            
        # Check if it's an ACL DOI
        if not doi.startswith(self.DOI_PREFIX):
            # Try case-insensitive match
            doi_lower = doi.lower()
            if not doi_lower.startswith(self.DOI_PREFIX.lower()):
                return None
        
        # Extract the anthology ID after the prefix
        anthology_id = doi[len(self.DOI_PREFIX):]
        return anthology_id if anthology_id else None
    
    def is_acl_doi(self, doi: str) -> bool:
        """Check if a DOI is from ACL Anthology.
        
        Args:
            doi: DOI to check
            
        Returns:
            True if it's an ACL DOI
        """
        return self._extract_anthology_id(doi) is not None
    
    async def download_by_doi(
        self,
        doi: str,
        output_path: Path,
    ) -> dict[str, Any] | None:
        """Download paper by DOI.
        
        Args:
            doi: ACL DOI (e.g., "10.18653/v1/N19-1423")
            output_path: Path to save the PDF
            
        Returns:
            Dict with 'pdf_path' and 'source' if successful, None otherwise
        """
        if not self.enabled:
            return None
            
        anthology_id = self._extract_anthology_id(doi)
        if not anthology_id:
            return None
        
        return await self.download_by_anthology_id(anthology_id, output_path)
    
    async def download_by_anthology_id(
        self,
        anthology_id: str,
        output_path: Path,
    ) -> dict[str, Any] | None:
        """Download paper by ACL Anthology ID.
        
        Args:
            anthology_id: ACL Anthology ID (e.g., "N19-1423", "2020.emnlp-main.1")
            output_path: Path to save the PDF
            
        Returns:
            Dict with 'pdf_path' and 'source' if successful, None otherwise
        """
        if not self.enabled:
            return None
            
        await self._rate_limit_wait()
        
        # Construct PDF URL
        # ACL Anthology format: https://aclanthology.org/{id}.pdf
        pdf_url = f"{self.BASE_URL}/{anthology_id}.pdf"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/pdf,*/*",
        }
        
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:
                response = await client.get(pdf_url, headers=headers)
                
                if response.status_code == 404:
                    return None
                    
                response.raise_for_status()
                
                content = response.content
                content_type = response.headers.get("content-type", "")
                
                # Verify it's a PDF
                if "pdf" not in content_type.lower() and not content.startswith(b"%PDF"):
                    return None
                    
                if len(content) < 1000:
                    return None
                
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(content)
                
                return {
                    "pdf_path": str(output_path),
                    "source": "acl_anthology",
                    "anthology_id": anthology_id,
                }
                
        except Exception:
            return None
    
    async def search_by_title(
        self,
        title: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Search ACL Anthology by title.
        
        Args:
            title: Paper title to search
            limit: Maximum results to return
            
        Returns:
            List of matching papers with anthology IDs
        """
        if not self.enabled:
            return []
            
        await self._rate_limit_wait()
        
        # ACL Anthology search API
        search_url = f"{self.BASE_URL}/search/"
        
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:
                # Search using query parameter
                params = {"q": title}
                response = await client.get(search_url, params=params)
                
                if response.status_code != 200:
                    return []
                
                # Parse results from HTML (simple extraction)
                results = self._parse_search_results(response.text, limit)
                return results
                
        except Exception:
            return []
    
    def _parse_search_results(self, html: str, limit: int) -> list[dict[str, Any]]:
        """Parse search results from ACL Anthology HTML.
        
        Args:
            html: HTML content from search page
            limit: Maximum results
            
        Returns:
            List of paper metadata
        """
        results = []
        
        # Look for paper links with anthology IDs
        # Pattern: /anthology/{id}/ or /{id}/ format
        patterns = [
            r'href="[^"]*?/([A-Z]\d{2}-\d{4})[/"]',  # Old format: N19-1423
            r'href="[^"]*?/(\d{4}\.[a-z]+-[a-z]+\.\d+)[/"]',  # New format: 2020.emnlp-main.1
        ]
        
        seen = set()
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for anthology_id in matches:
                if anthology_id not in seen and len(results) < limit:
                    seen.add(anthology_id)
                    results.append({
                        "anthology_id": anthology_id,
                        "pdf_url": f"{self.BASE_URL}/{anthology_id}.pdf",
                    })
        
        return results
    
    def is_available(self) -> bool:
        """Check if client is available.
        
        Returns:
            True if enabled
        """
        return self.enabled
