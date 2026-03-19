from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    niche: str = Field(min_length=2)
    geography: str = Field(min_length=2)
    keywords: list[str] = Field(default_factory=list)


class JobRead(BaseModel):
    id: int
    niche: str
    geography: str
    status: str
    total_candidates: int
    total_extracted: int
    total_valid: int
    created_at: datetime

    model_config = {"from_attributes": True}
