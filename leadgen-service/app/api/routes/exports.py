from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.repositories.job_repo import JobRepository
from app.repositories.lead_repo import LeadRepository
from app.schemas.export import ExportCreate, ExportRead
from app.services.exporter import ExporterService

router = APIRouter(tags=["exports"])


@router.post("/jobs/{job_id}/export", response_model=ExportRead, status_code=status.HTTP_201_CREATED)
def create_export(job_id: int, payload: ExportCreate, db: Session = Depends(get_db_session)) -> ExportRead:
    if payload.format != "csv":
        raise HTTPException(status_code=400, detail="Only csv export is supported")

    job_repo = JobRepository(db)
    job = job_repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    export_job = job_repo.create_export(job_id=job_id, format_name=payload.format)
    leads = LeadRepository(db).for_job(job_id)
    file_path = ExporterService().export_csv(job_id, leads)
    export_job.status = "completed"
    export_job.file_path = str(file_path)
    export_job.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(export_job)
    return export_job


@router.get("/exports/{export_id}", response_model=ExportRead)
def get_export(export_id: int, db: Session = Depends(get_db_session)) -> ExportRead:
    export = JobRepository(db).list_exports(export_id)
    if not export:
        raise HTTPException(status_code=404, detail="Export not found")
    return export
