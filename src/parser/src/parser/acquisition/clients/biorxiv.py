"""bioRxiv/medRxiv API client for preprint access."""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Any

import httpx

from .base import BaseClient, RateLimiter


class BioRxivClient(BaseClient):
    """Client for bioRxiv and medRxiv APIs.

    Provides access to preprints from:
    - bioRxiv: Biology preprints
    - medRxiv: Medical/health sciences preprints

    Both share DOI prefix 10.1101.
    
    Includes Selenium fallback for bot-protected downloads.
    """

    BIORXIV_API = "https://api.biorxiv.org/details"
    MEDRXIV_API = "https://api.medrxiv.org/details"

    def __init__(self, use_selenium: bool = True):
        """Initialize the bioRxiv client.
        
        Args:
            use_selenium: Whether to use Selenium for bot-protected downloads
        """
        super().__init__(
            base_url="https://api.biorxiv.org",
            rate_limiter=RateLimiter(calls_per_second=2.0)
        )
        self.use_selenium = use_selenium
        self._driver = None

    async def get_preprint(self, doi: str) -> dict[str, Any] | None:
        """Get preprint metadata and PDF URL.

        Args:
            doi: The DOI to look up. Must start with 10.1101 for bioRxiv/medRxiv.

        Returns:
            Dict with preprint info and PDF URL, or None if not found.
        """
        # bioRxiv/medRxiv DOIs start with 10.1101
        if not doi.startswith("10.1101"):
            return None

        async with httpx.AsyncClient(timeout=30) as client:
            for server, api in [
                ("biorxiv", self.BIORXIV_API),
                ("medrxiv", self.MEDRXIV_API),
            ]:
                try:
                    url = f"{api}/{server}/{doi}/na/json"
                    response = await client.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("collection"):
                            item = data["collection"][0]
                            return {
                                "title": item.get("title"),
                                "doi": doi,
                                "pdf_url": f"https://www.{server}.org/content/{doi}.full.pdf",
                                "server": server,
                                "authors": item.get("authors"),
                                "date": item.get("date"),
                                "category": item.get("category"),
                                "abstract": item.get("abstract"),
                            }
                except Exception:
                    continue

        return None

    async def download_pdf(self, doi: str, output_path: Path) -> bool:
        """Download PDF for a bioRxiv/medRxiv paper.
        
        Tries httpx first, falls back to Selenium if blocked.
        
        Args:
            doi: The DOI (must start with 10.1101)
            output_path: Path to save the PDF
            
        Returns:
            True if download succeeded
        """
        result = await self.get_preprint(doi)
        if not result or not result.get("pdf_url"):
            return False

        pdf_url = result["pdf_url"]
        output_path = Path(output_path)

        # Try httpx first with browser-like headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/pdf,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": f"https://www.{result['server']}.org/",
        }

        try:
            async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
                response = await client.get(pdf_url, headers=headers)

                if response.status_code == 200:
                    content = response.content
                    content_type = response.headers.get("content-type", "")

                    if "pdf" in content_type.lower() or content.startswith(b"%PDF"):
                        if len(content) > 1000:
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(content)
                            return True
        except Exception:
            pass

        # Fallback to Selenium if enabled
        if self.use_selenium:
            return await self._download_with_selenium(pdf_url, output_path)

        return False

    async def _download_with_selenium(self, pdf_url: str, output_path: Path) -> bool:
        """Download PDF using Selenium to bypass bot protection.
        
        Args:
            pdf_url: URL of the PDF
            output_path: Path to save the PDF
            
        Returns:
            True if download succeeded
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            return False

        loop = asyncio.get_event_loop()

        def do_download():
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            # Set up download directory
            download_dir = str(output_path.parent.absolute())
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True,
            }
            options.add_experimental_option("prefs", prefs)

            driver = None
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                driver.set_page_load_timeout(60)

                # Navigate to PDF URL
                driver.get(pdf_url)

                # Wait for potential CloudFlare challenge
                time.sleep(5)

                # Check if we're on a CloudFlare page
                page_source = driver.page_source.lower()
                if "cloudflare" in page_source or "checking your browser" in page_source:
                    # Wait longer for CloudFlare to resolve
                    time.sleep(10)

                # Try to get PDF content
                # bioRxiv might redirect or show inline PDF
                current_url = driver.current_url

                if ".pdf" in current_url:
                    # Direct PDF - use requests with cookies
                    cookies = {c['name']: c['value'] for c in driver.get_cookies()}

                    import requests
                    session = requests.Session()
                    for name, value in cookies.items():
                        session.cookies.set(name, value)

                    response = session.get(pdf_url, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }, timeout=60)

                    if response.status_code == 200 and (
                        "pdf" in response.headers.get("content-type", "").lower() or
                        response.content.startswith(b"%PDF")
                    ):
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        output_path.write_bytes(response.content)
                        return True

                # Check for downloaded file in download directory
                time.sleep(3)
                for f in Path(download_dir).glob("*.pdf"):
                    if f.stat().st_mtime > time.time() - 30:  # Recent file
                        if f != output_path:
                            f.rename(output_path)
                        return True

                return False

            except Exception:
                return False
            finally:
                if driver:
                    try:
                        driver.quit()
                    except Exception:
                        pass

        return await loop.run_in_executor(None, do_download)

    async def get_pdf_url(self, doi: str) -> str | None:
        """Get PDF URL for a bioRxiv/medRxiv DOI.

        Args:
            doi: The DOI to look up.

        Returns:
            PDF URL or None if not found.
        """
        result = await self.get_preprint(doi)
        if result:
            return result.get("pdf_url")
        return None

    async def search_by_date_range(
        self,
        server: str,
        start_date: str,
        end_date: str,
        cursor: int = 0,
    ) -> dict[str, Any]:
        """Search for preprints by date range.

        Args:
            server: Either 'biorxiv' or 'medrxiv'.
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.
            cursor: Pagination cursor.

        Returns:
            Dict with collection of results and message info.
        """
        base_url = self.BIORXIV_API if server == "biorxiv" else self.MEDRXIV_API
        url = f"{base_url}/{server}/{start_date}/{end_date}/{cursor}/json"

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception:
            return {"collection": [], "messages": []}

    async def search_by_title(
        self,
        title: str,
        server: str = "biorxiv",
        max_results: int = 10,
    ) -> list[dict[str, Any]]:
        """Search preprints by title (approximate).

        Note: bioRxiv API doesn't have direct title search, so this
        searches recent preprints and filters by title similarity.
        For accurate title search, use CrossRef or Semantic Scholar.

        Args:
            title: Title to search for.
            server: 'biorxiv' or 'medrxiv'.
            max_results: Maximum results.

        Returns:
            List of matching preprints.
        """
        # bioRxiv API is limited - search recent dates
        # For real title search, recommend using CrossRef
        import datetime

        end_date = datetime.date.today().isoformat()
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

        results = await self.search_by_date_range(server, start_date, end_date)

        # Filter by title similarity
        title_lower = title.lower()
        matches = []

        for item in results.get("collection", []):
            item_title = item.get("title", "").lower()
            # Simple substring match
            if title_lower in item_title or item_title in title_lower:
                matches.append({
                    "title": item.get("title"),
                    "doi": item.get("doi"),
                    "pdf_url": f"https://www.{server}.org/content/{item.get('doi')}.full.pdf",
                    "server": server,
                    "authors": item.get("authors"),
                    "date": item.get("date"),
                })
                if len(matches) >= max_results:
                    break

        return matches

    async def get_paper_metadata(self, identifier: str) -> dict[str, Any] | None:
        """Get metadata for a paper by DOI.

        Args:
            identifier: The DOI (must start with 10.1101 for bioRxiv/medRxiv).

        Returns:
            Paper metadata dict or None.
        """
        return await self.get_preprint(identifier)
