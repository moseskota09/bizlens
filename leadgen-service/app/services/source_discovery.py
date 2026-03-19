from dataclasses import dataclass


@dataclass(slots=True)
class CandidateSource:
    source_url: str
    website: str
    source_name: str


class SourceDiscoveryService:
    """Placeholder adapter that should only call permitted APIs/sources."""

    def discover(self, niche: str, geography: str, keywords: list[str]) -> list[CandidateSource]:
        seed = f"https://example.com/search?q={niche}+{geography}"
        website = f"https://www.example-{niche.replace(' ', '-').lower()}.com"
        return [CandidateSource(source_url=seed, website=website, source_name="placeholder_public_directory")]
