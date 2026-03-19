from datetime import datetime

from pydantic import BaseModel


class ExportCreate(BaseModel):
    format: str = "csv"


class ExportRead(BaseModel):
    id: int
    job_id: int
    format: str
    status: str
    file_path: str | None
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}
