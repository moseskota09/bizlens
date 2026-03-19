from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.repositories.job_repo import JobRepository
from app.repositories.lead_repo import LeadRepository
from app.schemas.job import JobCreate, JobRead
from app.schemas.lead import LeadRead
from app.workers.tasks import process_source_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db_session)) -> JobRead:
    repo = JobRepository(db)
    job = repo.create(payload)
    try:
        process_source_job.delay(job.id)
    except Exception:
        process_source_job(job.id)
    return job


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: int, db: Session = Depends(get_db_session)) -> JobRead:
    repo = JobRepository(db)
    job = repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}/leads", response_model=list[LeadRead])
def list_job_leads(job_id: int, db: Session = Depends(get_db_session)) -> list[LeadRead]:
    job_repo = JobRepository(db)
    if not job_repo.get(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    repo = LeadRepository(db)
    return repo.for_job(job_id)
