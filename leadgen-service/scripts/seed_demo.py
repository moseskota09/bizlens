from app.core.database import SessionLocal
from app.repositories.job_repo import JobRepository
from app.schemas.job import JobCreate


def main() -> None:
    db = SessionLocal()
    try:
        job = JobRepository(db).create(JobCreate(niche="dentist", geography="Miami, FL", keywords=["family"]))
        print(f"Created job {job.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
