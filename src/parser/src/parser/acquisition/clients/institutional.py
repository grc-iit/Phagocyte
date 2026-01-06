"""Institutional access client using EZProxy and VPN.

Supports two modes for accessing papers via university subscriptions:
1. VPN mode: When connected to institutional VPN, direct access works
2. EZProxy mode: Uses proxy URL rewriting with browser-based authentication
"""

from __future__ import annotations

import asyncio
import contextlib
import pickle
import subprocess
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


class InstitutionalAccessClient:
    """Client for accessing papers through institutional proxy (EZProxy).

    Supports two modes:
    1. VPN mode: When connected to institutional VPN, direct access works
    2. EZProxy mode: Uses proxy URL rewriting with Selenium authentication
    """

    def __init__(
        self,
        proxy_url: str | None = None,
        vpn_enabled: bool = False,
        vpn_script: str | None = None,
        vpn_disconnect_script: str | None = None,
        cookies_file: str = ".institutional_cookies.pkl",
        download_dir: str = "./downloads",
        rate_limit: float = 1.0,
    ):
        """Initialize the institutional access client.

        Args:
            proxy_url: EZProxy URL (e.g., "https://ezproxy.gl.iit.edu/login?url=")
            vpn_enabled: If True, assume VPN is connected and use direct access
            vpn_script: Path to script that connects to VPN (run during auth)
            vpn_disconnect_script: Path to script that disconnects VPN
            cookies_file: Path to save/load authentication cookies
            download_dir: Directory to save downloaded PDFs
            rate_limit: Seconds between requests
        """
        self.proxy_url = proxy_url
        self.vpn_enabled = vpn_enabled
        self.vpn_script = vpn_script
        self.vpn_disconnect_script = vpn_disconnect_script
        self.cookies_file = Path(cookies_file)
        self.download_dir = Path(download_dir)
        self.rate_limit = rate_limit
        self._cookies: dict[str, str] = {}
        self._selenium_cookies: list[dict] = []
        self._authenticated = False
        self._vpn_connected = False
        self._last_error: str | None = None
        self._last_request: float = 0.0

        # Auto-load cookies if they exist
        if self.cookies_file.exists():
            self.load_cookies()

    async def _rate_limit(self) -> None:
        """Wait to respect rate limits."""
        now = time.time()
        elapsed = now - self._last_request
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self._last_request = time.time()

    def get_proxied_url(self, url: str) -> str:
        """Convert a URL to a proxied URL.

        Args:
            url: Original URL (e.g., DOI URL or publisher URL)

        Returns:
            Proxied URL if proxy is configured, otherwise original URL
        """
        if self.vpn_enabled:
            return url

        if self.proxy_url:
            return f"{self.proxy_url}{url}"

        return url

    def doi_to_proxied_url(self, doi: str) -> str:
        """Convert a DOI to a proxied publisher URL.

        Args:
            doi: The DOI to convert

        Returns:
            Proxied URL for the DOI
        """
        doi_url = f"https://doi.org/{doi}"
        return self.get_proxied_url(doi_url)

    def load_cookies(self) -> bool:
        """Load previously saved authentication cookies.

        Returns:
            True if cookies were loaded successfully
        """
        if not self.cookies_file.exists():
            return False

        try:
            with open(self.cookies_file, "rb") as f:
                data = pickle.load(f)

            # Handle both old format (dict) and new format (dict with selenium_cookies)
            if isinstance(data, dict) and "selenium_cookies" in data:
                self._selenium_cookies = data["selenium_cookies"]
                self._cookies = data["simple_cookies"]
            elif isinstance(data, dict):
                # Old format - just simple cookies
                self._cookies = data
                self._selenium_cookies = []
            else:
                return False

            self._authenticated = True
            return True
        except (pickle.PickleError, EOFError):
            return False

    def save_cookies(self) -> None:
        """Save authentication cookies for reuse."""
        data = {
            "selenium_cookies": self._selenium_cookies,
            "simple_cookies": self._cookies,
        }
        with open(self.cookies_file, "wb") as f:
            pickle.dump(data, f)

    def connect_vpn(self) -> bool:
        """Run the VPN connection script.

        Returns:
            True if VPN connected successfully (or no script configured)
        """
        if not self.vpn_script:
            print("No VPN script configured.")
            return False

        script_path = Path(self.vpn_script)
        if not script_path.exists():
            print(f"VPN script not found: {self.vpn_script}")
            return False

        print(f"\nRunning VPN script: {self.vpn_script}")
        print("=" * 60)

        try:
            # Run the script
            result = subprocess.run(
                [str(script_path)],
                shell=True,
                capture_output=False,  # Let output go to terminal for interactive scripts
                text=True,
            )

            if result.returncode == 0:
                print("=" * 60)
                print("VPN script completed successfully.")
                self._vpn_connected = True
                self._authenticated = True
                return True
            else:
                print("=" * 60)
                print(f"VPN script failed with exit code: {result.returncode}")
                return False

        except Exception as e:
            print(f"Error running VPN script: {e}")
            return False

    def disconnect_vpn(self) -> bool:
        """Run a VPN disconnect script if provided.

        Returns:
            True if disconnect was successful
        """
        if not self.vpn_disconnect_script:
            self._vpn_connected = False
            return True

        script_path = Path(self.vpn_disconnect_script)
        if not script_path.exists():
            print(f"Disconnect script not found: {self.vpn_disconnect_script}")
            return False

        try:
            result = subprocess.run(
                [str(script_path)],
                shell=True,
                capture_output=True,
                text=True,
            )
            self._vpn_connected = False
            return result.returncode == 0
        except Exception as e:
            print(f"Error running disconnect script: {e}")
            return False

    def _check_selenium_available(self) -> bool:
        """Check if Selenium is available."""
        try:
            from selenium import webdriver  # noqa: F401
            return True
        except ImportError:
            return False

    def _get_available_browser(self) -> tuple[Any, str] | None:
        """Detect and return an available browser driver.

        Tries browsers in order: Chrome, Edge, Firefox.
        Returns the first one that works.

        Returns:
            Tuple of (driver, browser_name) or None if no browser available.
        """
        if not self._check_selenium_available():
            return None

        from selenium import webdriver

        browsers = [
            ("chrome", self._try_chrome),
            ("edge", self._try_edge),
            ("firefox", self._try_firefox),
        ]

        for name, try_func in browsers:
            try:
                driver = try_func(webdriver)
                if driver:
                    return driver, name
            except Exception:
                continue

        return None

    def _try_chrome(self, webdriver: Any) -> Any | None:
        """Try to create a Chrome driver."""
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        options = Options()
        options.add_argument("--start-maximized")

        # Try with webdriver-manager first
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)
        except Exception:
            pass

        # Try without webdriver-manager
        try:
            return webdriver.Chrome(options=options)
        except Exception:
            return None

    def _try_edge(self, webdriver: Any) -> Any | None:
        """Try to create an Edge driver."""
        from selenium.webdriver.edge.options import Options
        from selenium.webdriver.edge.service import Service

        options = Options()
        options.add_argument("--start-maximized")

        # Try with webdriver-manager first
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            service = Service(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service, options=options)
        except Exception:
            pass

        # Try without webdriver-manager
        try:
            return webdriver.Edge(options=options)
        except Exception:
            return None

    def _try_firefox(self, webdriver: Any) -> Any | None:
        """Try to create a Firefox driver."""
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.service import Service

        options = Options()

        # Try with webdriver-manager first
        try:
            from webdriver_manager.firefox import GeckoDriverManager
            service = Service(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
        except Exception:
            pass

        # Try without webdriver-manager
        try:
            return webdriver.Firefox(options=options)
        except Exception:
            return None

    def authenticate_interactive(self) -> bool:
        """Authenticate using an interactive browser session.

        Opens a browser window for the user to log in through their
        institution's SSO/Shibboleth system. Saves cookies for reuse.

        Returns:
            True if authentication was successful
        """
        if not self._check_selenium_available():
            raise ImportError(
                "Selenium is required for EZProxy authentication. "
                "Install with: pip install selenium webdriver-manager"
            )

        if not self.proxy_url:
            print("No proxy URL configured. Cannot authenticate.")
            return False

        print("\n" + "=" * 60)
        print("Institutional Authentication (EZProxy)")
        print("=" * 60)
        print("\nOpening browser for institutional login...")
        print("Please log in with your university credentials.")
        print("The browser will close automatically when done.")
        print()

        browser_result = self._get_available_browser()
        if not browser_result:
            print("No supported browser found (Chrome, Edge, or Firefox)")
            return False

        driver, browser_name = browser_result
        print(f"Using {browser_name} browser")

        try:
            # Navigate to a test URL through the proxy
            test_url = self.get_proxied_url("https://www.nature.com/")
            driver.get(test_url)

            print("\nWaiting for login to complete...")
            print("(The browser will close automatically after login)")

            # Wait for authentication - check for successful proxy session
            max_wait = 300  # 5 minutes
            check_interval = 2
            elapsed = 0

            while elapsed < max_wait:
                time.sleep(check_interval)
                elapsed += check_interval

                current_url = driver.current_url
                parsed = urlparse(current_url)

                # Check if we've passed through the proxy and are on a publisher site
                # EZProxy rewrites domains like nature-com.ezproxy.gl.iit.edu
                if ("ezproxy" in parsed.netloc.lower() and "login" not in current_url.lower() and
                    any(x in parsed.netloc.lower() for x in ["nature", "ieee", "acm", "springer", "elsevier", "wiley"])):
                    print(f"\nReached proxied site: {parsed.netloc}")
                    break

                # Also check for direct publisher access (some EZProxy setups)
                if any(x in current_url.lower() for x in ["nature.com", "ieee.org", "acm.org"]) and "login" not in current_url.lower():
                    break

            # Collect all cookies from all domains
            all_cookies = driver.get_cookies()
            print(f"\nCollected {len(all_cookies)} cookies")

            # Save cookies
            self._selenium_cookies = all_cookies
            self._cookies = {c["name"]: c["value"] for c in self._selenium_cookies}
            self.save_cookies()

            self._authenticated = True
            print("Authentication successful! Cookies saved.")
            return True

        except Exception as e:
            print(f"Authentication error: {e}")
            self._last_error = str(e)
            return False

        finally:
            with contextlib.suppress(Exception):
                driver.quit()

    async def get_pdf_url(self, doi: str) -> str | None:
        """Get PDF URL through institutional access.

        Args:
            doi: Paper DOI

        Returns:
            Proxied URL for accessing the paper, or None
        """
        if not self._authenticated and not self.vpn_enabled:
            return None

        await self._rate_limit()

        # Return the proxied DOI URL
        return self.doi_to_proxied_url(doi)

    async def download_pdf(
        self,
        doi: str,
        output_path: Path | None = None,
    ) -> Path | None:
        """Download a PDF through institutional access.

        In VPN mode, uses direct HTTP with browser-like headers.
        In EZProxy mode, requires Selenium for browser-based download.

        Args:
            doi: Paper DOI
            output_path: Where to save the PDF

        Returns:
            Path to downloaded PDF, or None if failed
        """
        if not self._authenticated and not self.vpn_enabled:
            print("Not authenticated. Run authenticate_interactive() first.")
            return None

        await self._rate_limit()

        # VPN mode - try direct download with httpx
        if self.vpn_enabled:
            import httpx

            doi_url = f"https://doi.org/{doi}"
            output_path = Path(output_path) if output_path else self.download_dir / f"{doi.replace('/', '_')}.pdf"
            output_path.parent.mkdir(parents=True, exist_ok=True)

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,application/pdf,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            }

            try:
                async with httpx.AsyncClient(
                    timeout=60.0,
                    follow_redirects=True,
                    headers=headers,
                ) as client:
                    # First resolve the DOI to get the publisher URL
                    response = await client.get(doi_url)
                    final_url = str(response.url)

                    # Try to find PDF link on the page
                    pdf_url = self._find_pdf_link(response.text, final_url)

                    if pdf_url:
                        # Download the PDF
                        pdf_response = await client.get(pdf_url)
                        content = pdf_response.content

                        if content.startswith(b"%PDF") and len(content) > 1000:
                            output_path.write_bytes(content)
                            return output_path

                    # Try common PDF URL patterns
                    pdf_patterns = [
                        final_url.replace("/abs/", "/pdf/"),
                        final_url.replace("/full/", "/pdf/"),
                        final_url + ".pdf",
                        final_url.replace(".html", ".pdf"),
                    ]

                    for pattern_url in pdf_patterns:
                        if pattern_url != final_url:
                            try:
                                pdf_response = await client.get(pattern_url)
                                content = pdf_response.content
                                if content.startswith(b"%PDF") and len(content) > 1000:
                                    output_path.write_bytes(content)
                                    return output_path
                            except Exception:
                                continue

            except Exception as e:
                self._last_error = str(e)
                return None

            return None

        # EZProxy mode - use httpx with saved cookies
        return await self._download_via_ezproxy(doi, output_path)

    async def _download_via_ezproxy(
        self,
        doi: str,
        output_path: Path | None = None,
    ) -> Path | None:
        """Download PDF via EZProxy using saved cookies.

        Args:
            doi: Paper DOI
            output_path: Where to save the PDF

        Returns:
            Path to downloaded PDF, or None if failed
        """
        import httpx

        output_path = Path(output_path) if output_path else self.download_dir / f"{doi.replace('/', '_')}.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert Selenium cookies to httpx format (strip leading dots from domains)
        cookies = httpx.Cookies()
        for cookie in self._selenium_cookies:
            domain = cookie.get("domain", "").lstrip(".")
            cookies.set(
                cookie["name"],
                cookie["value"],
                domain=domain,
            )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,application/pdf,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            proxied_url = self.doi_to_proxied_url(doi)

            async with httpx.AsyncClient(
                timeout=60.0,
                follow_redirects=True,
                headers=headers,
                cookies=cookies,
                verify=False,  # Skip SSL verification for EZProxy
            ) as client:
                # Navigate through EZProxy to the publisher
                response = await client.get(proxied_url)
                final_url = str(response.url)
                html = response.text

                # Try to find PDF link on the page using meta tag first (most reliable)
                pdf_url = self._find_pdf_link(html, final_url)

                if pdf_url:
                    # Handle relative URLs
                    if pdf_url.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(final_url)
                        pdf_url = f"{parsed.scheme}://{parsed.netloc}{pdf_url}"

                    pdf_response = await client.get(pdf_url)
                    content = pdf_response.content

                    if content.startswith(b"%PDF") and len(content) > 1000:
                        output_path.write_bytes(content)
                        return output_path

                # Try Nature-specific PDF patterns
                if "nature" in final_url.lower():
                    # Nature uses /articles/xxx.pdf pattern
                    nature_patterns = [
                        final_url.replace("/articles/", "/articles/") + ".pdf",
                        final_url + ".pdf",
                        final_url.replace(".html", ".pdf"),
                    ]
                    for pattern_url in nature_patterns:
                        if pattern_url != final_url:
                            try:
                                if self.proxy_url and "ezproxy" not in pattern_url.lower():
                                    pattern_url = self.get_proxied_url(pattern_url)
                                pdf_response = await client.get(pattern_url)
                                content = pdf_response.content
                                if content.startswith(b"%PDF") and len(content) > 1000:
                                    output_path.write_bytes(content)
                                    return output_path
                            except Exception:
                                continue

                # Try common PDF URL patterns
                pdf_patterns = [
                    final_url.replace("/abs/", "/pdf/"),
                    final_url.replace("/full/", "/pdf/"),
                    final_url + ".pdf",
                    final_url.replace(".html", ".pdf"),
                ]

                for pattern_url in pdf_patterns:
                    if pattern_url != final_url:
                        try:
                            if self.proxy_url and "ezproxy" not in pattern_url.lower():
                                pattern_url = self.get_proxied_url(pattern_url)
                            pdf_response = await client.get(pattern_url)
                            content = pdf_response.content
                            if content.startswith(b"%PDF") and len(content) > 1000:
                                output_path.write_bytes(content)
                                return output_path
                        except Exception:
                            continue

        except Exception as e:
            self._last_error = str(e)
            return None

        return None

    def _find_pdf_link(self, html: str, base_url: str) -> str | None:
        """Find PDF link in HTML page.

        Args:
            html: HTML content
            base_url: Base URL for relative links

        Returns:
            PDF URL or None
        """
        import re
        from urllib.parse import urljoin

        patterns = [
            r'<a[^>]+href="([^"]+\.pdf[^"]*)"[^>]*>.*?(?:PDF|Download)',
            r'<a[^>]+href="([^"]+)"[^>]*class="[^"]*pdf[^"]*"',
            r'data-pdf-url="([^"]+)"',
            r'"pdfUrl"\s*:\s*"([^"]+)"',
            r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                url = match.group(1)
                if url.startswith("/") or not url.startswith("http"):
                    url = urljoin(base_url, url)
                return url

        return None

    def is_authenticated(self) -> bool:
        """Check if we have valid authentication.

        Returns:
            True if authenticated (via cookies or VPN)
        """
        return self._authenticated or self.vpn_enabled

    def is_available(self) -> bool:
        """Check if institutional access is available.

        Returns:
            True if proxy URL or VPN is configured
        """
        return bool(self.proxy_url) or self.vpn_enabled

    @property
    def last_error(self) -> str | None:
        """Get the last error message."""
        return self._last_error
