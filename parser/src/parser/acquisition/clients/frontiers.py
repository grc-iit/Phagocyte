"""Frontiers client for downloading open access papers.

Frontiers is a Gold Open Access publisher - all papers are freely available.
However, they use aggressive bot protection (CloudFlare) which requires
Selenium to bypass.

DOI format: 10.3389/{journal}.{year}.{id}
Example: 10.3389/fimmu.2021.737524
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Any

import httpx


class FrontiersClient:
    """Client for downloading papers from Frontiers.
    
    Frontiers journals include:
    - Frontiers in Immunology (fimmu)
    - Frontiers in Neuroscience (fnins)
    - Frontiers in Microbiology (fmicb)
    - Frontiers in Psychology (fpsyg)
    - And many more...
    
    All papers are Gold Open Access but protected by CloudFlare.
    """
    
    BASE_URL = "https://www.frontiersin.org"
    DOI_PREFIX = "10.3389/"
    
    def __init__(
        self,
        enabled: bool = True,
        timeout: float = 60.0,
        use_selenium: bool = True,
    ):
        """Initialize the Frontiers client.
        
        Args:
            enabled: Whether the client is enabled
            timeout: Request timeout in seconds
            use_selenium: Whether to use Selenium for bot protection bypass
        """
        self.enabled = enabled
        self.timeout = timeout
        self.use_selenium = use_selenium
    
    def is_frontiers_doi(self, doi: str) -> bool:
        """Check if a DOI is from Frontiers.
        
        Args:
            doi: DOI to check
            
        Returns:
            True if it's a Frontiers DOI
        """
        return doi.startswith(self.DOI_PREFIX) if doi else False
    
    def _get_pdf_url(self, doi: str) -> str:
        """Construct PDF URL from DOI.
        
        Args:
            doi: Frontiers DOI
            
        Returns:
            Direct PDF URL
        """
        # Frontiers PDF URL format:
        # https://www.frontiersin.org/articles/10.3389/fimmu.2021.737524/pdf
        return f"{self.BASE_URL}/articles/{doi}/pdf"
    
    def _get_article_url(self, doi: str) -> str:
        """Construct article page URL from DOI.
        
        Args:
            doi: Frontiers DOI
            
        Returns:
            Article page URL
        """
        return f"{self.BASE_URL}/articles/{doi}/full"
    
    async def download_by_doi(
        self,
        doi: str,
        output_path: Path,
    ) -> dict[str, Any] | None:
        """Download paper by DOI.
        
        Args:
            doi: Frontiers DOI (e.g., "10.3389/fimmu.2021.737524")
            output_path: Path to save the PDF
            
        Returns:
            Dict with 'pdf_path' and 'source' if successful, None otherwise
        """
        if not self.enabled:
            return None
        
        if not self.is_frontiers_doi(doi):
            return None
        
        output_path = Path(output_path)
        pdf_url = self._get_pdf_url(doi)
        
        # Try httpx first with browser-like headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/pdf,text/html,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": self._get_article_url(doi),
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
        }
        
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:
                response = await client.get(pdf_url, headers=headers)
                
                if response.status_code == 200:
                    content = response.content
                    content_type = response.headers.get("content-type", "")
                    
                    # Check if we got a PDF
                    if "pdf" in content_type.lower() or content.startswith(b"%PDF"):
                        if len(content) > 1000:
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(content)
                            return {
                                "pdf_path": str(output_path),
                                "source": "frontiers",
                            }
        except Exception:
            pass
        
        # Fallback to Selenium if enabled
        if self.use_selenium:
            return await self._download_with_selenium(doi, output_path)
        
        return None
    
    async def _download_with_selenium(
        self,
        doi: str,
        output_path: Path,
    ) -> dict[str, Any] | None:
        """Download PDF using Selenium to bypass CloudFlare.
        
        Args:
            doi: Frontiers DOI
            output_path: Path to save the PDF
            
        Returns:
            Result dict or None
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            return None
        
        pdf_url = self._get_pdf_url(doi)
        article_url = self._get_article_url(doi)
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
                
                # First visit the article page to get cookies
                driver.get(article_url)
                time.sleep(3)
                
                # Check for CloudFlare challenge
                page_source = driver.page_source.lower()
                if "cloudflare" in page_source or "checking your browser" in page_source:
                    # Wait for CloudFlare to resolve
                    time.sleep(10)
                
                # Now try to access the PDF
                driver.get(pdf_url)
                time.sleep(5)
                
                # Check if we're still on CloudFlare
                page_source = driver.page_source.lower()
                if "cloudflare" in page_source:
                    time.sleep(10)
                
                # Get cookies and try direct download
                cookies = {c['name']: c['value'] for c in driver.get_cookies()}
                
                import requests
                session = requests.Session()
                for name, value in cookies.items():
                    session.cookies.set(name, value)
                
                response = session.get(pdf_url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": article_url,
                }, timeout=60, allow_redirects=True)
                
                if response.status_code == 200:
                    content = response.content
                    if "pdf" in response.headers.get("content-type", "").lower() or content.startswith(b"%PDF"):
                        if len(content) > 1000:
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(content)
                            return {"pdf_path": str(output_path), "source": "frontiers"}
                
                # Check for downloaded file
                time.sleep(3)
                for f in Path(download_dir).glob("*.pdf"):
                    if f.stat().st_mtime > time.time() - 30:
                        if f != output_path:
                            f.rename(output_path)
                        return {"pdf_path": str(output_path), "source": "frontiers"}
                
                return None
                
            except Exception:
                return None
            finally:
                if driver:
                    try:
                        driver.quit()
                    except Exception:
                        pass
        
        return await loop.run_in_executor(None, do_download)
    
    def is_available(self) -> bool:
        """Check if client is available.
        
        Returns:
            True if enabled
        """
        return self.enabled
