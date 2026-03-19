from datetime import datetime

from pydantic import BaseModel


class LeadRead(BaseModel):
    id: int
    job_id: int
    business_name: str | None
    website: str
    root_domain: str | None
    city: str | None
    state: str | None
    category: str | None
    phone: str | None
    email: str | None
    contact_page_url: str | None
    summary: str | None
    personalization_line: str | None
    lead_score: float
    source_url: str
    extraction_method: str
    is_valid: bool
    validation_notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
