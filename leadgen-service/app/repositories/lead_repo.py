from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lead import Lead


class LeadRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, lead: Lead) -> Lead:
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def for_job(self, job_id: int) -> list[Lead]:
        statement = select(Lead).where(Lead.job_id == job_id)
        return list(self.db.scalars(statement))
