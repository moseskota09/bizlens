import json
from datetime import datetime

from app.core.database import SessionLocal
from app.models.lead import Lead
from app.repositories.job_repo import JobRepository
from app.repositories.lead_repo import LeadRepository
from app.schemas.job import JobCreate
from app.services.enricher import EnricherService
from app.services.extractor import ExtractorService
from app.services.normalizer import NormalizerService
from app.services.page_fetcher import PageFetcher
from app.services.scorer import ScorerService
from app.services.source_discovery import SourceDiscoveryService
from app.services.validator import ValidatorService
from app.workers.queue import celery_app


@celery_app.task(name="process_source_job")
def process_source_job(job_id: int) -> None:
    db = SessionLocal()
    try:
        job_repo = JobRepository(db)
        lead_repo = LeadRepository(db)
        job = job_repo.get(job_id)
        if not job:
            return

        job.status = "running"
        db.commit()
        keywords = json.loads(job.keywords_json)

        discovery = SourceDiscoveryService()
        fetcher = PageFetcher()
        extractor = ExtractorService()
        normalizer = NormalizerService()
        validator = ValidatorService()
        scorer = ScorerService()
        enricher = EnricherService()

        candidates = discovery.discover(job.niche, job.geography, keywords)
        job.total_candidates = len(candidates)
        db.commit()

        for candidate in candidates:
            try:
                page = fetcher.fetch(candidate.website)
            except Exception:
                continue
            fields = extractor.extract(candidate.website, page.html)
            lead = normalizer.normalize(
                job_id=job.id,
                website=candidate.website,
                source_url=candidate.source_url,
                fields=fields,
                method=page.method,
            )
            lead = validator.validate(lead)
            lead = scorer.score(lead)
            enrich = enricher.enrich(lead.business_name, fields.text_excerpt)
            lead.summary = enrich.summary
            lead.personalization_line = enrich.personalization_line
            lead_repo.create(lead)

        leads = lead_repo.for_job(job.id)
        job.total_extracted = len(leads)
        job.total_valid = sum(1 for l in leads if l.is_valid)
        job.status = "completed"
        job.completed_at = datetime.utcnow()
        db.commit()
    finally:
        db.close()
