from dataclasses import dataclass

import httpx

from app.core.config import get_settings
from app.core.security import validate_public_http_url


@dataclass(slots=True)
class PageContent:
    url: str
    html: str
    method: str


class PageFetcher:
    def __init__(self) -> None:
        self.settings = get_settings()

    def fetch(self, url: str) -> PageContent:
        safe_url = validate_public_http_url(url)
        headers = {"User-Agent": self.settings.user_agent}
        with httpx.Client(timeout=self.settings.request_timeout_seconds, follow_redirects=True, headers=headers) as client:
            response = client.get(safe_url)
            response.raise_for_status()
        return PageContent(url=safe_url, html=response.text, method="http")

    def fetch_with_playwright(self, url: str) -> PageContent:
        safe_url = validate_public_http_url(url)
        if not self.settings.allow_playwright_fallback:
            raise RuntimeError("Playwright fallback disabled")
        return PageContent(url=safe_url, html="", method="playwright_placeholder")
