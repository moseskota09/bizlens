import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.export_job import ExportJob
from app.models.source_job import SourceJob
from app.schemas.job import JobCreate


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: JobCreate) -> SourceJob:
        job = SourceJob(niche=payload.niche, geography=payload.geography, keywords_json=json.dumps(payload.keywords))
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get(self, job_id: int) -> SourceJob | None:
        return self.db.get(SourceJob, job_id)

    def list_exports(self, export_id: int) -> ExportJob | None:
        return self.db.get(ExportJob, export_id)

    def create_export(self, job_id: int, format_name: str) -> ExportJob:
        export = ExportJob(job_id=job_id, format=format_name)
        self.db.add(export)
        self.db.commit()
        self.db.refresh(export)
        return export

    def set_status(self, job_id: int, status: str) -> None:
        job = self.get(job_id)
        if not job:
            return
        job.status = status
        self.db.commit()

    def jobs(self) -> list[SourceJob]:
        return list(self.db.scalars(select(SourceJob)))
