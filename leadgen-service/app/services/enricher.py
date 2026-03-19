from dataclasses import dataclass

from app.core.config import get_settings

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


@dataclass(slots=True)
class EnrichmentResult:
    summary: str
    personalization_line: str


class EnricherService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def enrich(self, business_name: str | None, text_excerpt: str) -> EnrichmentResult:
        if not self.settings.openai_api_key or OpenAI is None:
            name = business_name or "This business"
            return EnrichmentResult(
                summary=f"{name} appears to operate a local business website.",
                personalization_line=f"Noticed your website and thought a local lead pipeline could help {name}.",
            )

        client = OpenAI(api_key=self.settings.openai_api_key)
        prompt = (
            "Create a concise business summary and one personalized outreach line. "
            f"Business name: {business_name or 'Unknown'}. Content: {text_excerpt[:2000]}"
        )
        response = client.responses.create(
            model=self.settings.openai_model,
            input=prompt,
            temperature=0.2,
        )
        text = response.output_text.strip()
        lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
        summary = lines[0] if lines else "Summary unavailable"
        personalization = lines[1] if len(lines) > 1 else "Personalization line unavailable"
        return EnrichmentResult(summary=summary, personalization_line=personalization)
