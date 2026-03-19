from app.models.lead import Lead
from app.services.extractor import ExtractedFields, root_domain_for_url


class NormalizerService:
    def normalize(self, *, job_id: int, website: str, source_url: str, fields: ExtractedFields, method: str) -> Lead:
        return Lead(
            job_id=job_id,
            website=website,
            source_url=source_url,
            root_domain=root_domain_for_url(website),
            business_name=fields.business_name,
            phone=self._normalize_phone(fields.phone),
            email=fields.email.lower() if fields.email else None,
            contact_page_url=fields.contact_page_url,
            extraction_method=method,
        )

    def _normalize_phone(self, phone: str | None) -> str | None:
        if not phone:
            return None
        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) == 10:
            return f"+1{digits}"
        if len(digits) == 11 and digits[0] == "1":
            return f"+{digits}"
        return phone
