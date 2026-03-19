from urllib.parse import urlparse

from app.models.lead import Lead


class ValidatorService:
    def validate(self, lead: Lead) -> Lead:
        notes: list[str] = []
        if not lead.email and not lead.phone and not lead.contact_page_url:
            notes.append("No reachable contact method found")
        if urlparse(lead.website).scheme not in {"http", "https"}:
            notes.append("Unsupported URL scheme")

        lead.is_valid = len(notes) == 0
        lead.validation_notes = "; ".join(notes) if notes else "valid"
        return lead
