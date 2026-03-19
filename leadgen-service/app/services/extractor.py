import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}")


@dataclass(slots=True)
class ExtractedFields:
    business_name: str | None
    email: str | None
    phone: str | None
    contact_page_url: str | None
    text_excerpt: str


class ExtractorService:
    def extract(self, website: str, html: str) -> ExtractedFields:
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.string.strip() if soup.title and soup.title.string else None
        text = soup.get_text(" ", strip=True)
        email_match = EMAIL_RE.search(text)
        phone_match = PHONE_RE.search(text)
        contact_url = self._find_contact_url(website, soup)
        return ExtractedFields(
            business_name=title,
            email=email_match.group(0) if email_match else None,
            phone=phone_match.group(0) if phone_match else None,
            contact_page_url=contact_url,
            text_excerpt=text[:5000],
        )

    def _find_contact_url(self, website: str, soup: BeautifulSoup) -> str | None:
        for a_tag in soup.select("a[href]"):
            href = (a_tag.get("href") or "").strip()
            label = a_tag.get_text(" ", strip=True).lower()
            target = href.lower()
            if "contact" in label or "contact" in target:
                return urljoin(website, href)
        return None


def root_domain_for_url(url: str) -> str | None:
    host = urlparse(url).hostname
    return host.lower() if host else None
