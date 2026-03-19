# LeadGen Service MVP

Production-oriented scaffold for compliant local business lead generation.

## Features

- FastAPI endpoints for health, jobs, leads listing, and exports.
- SQLAlchemy models for `source_jobs`, `leads`, and `export_jobs`.
- Celery + Redis worker orchestration.
- SSRF-aware page fetching with private network blocking.
- HTML extraction for business title, contact email/phone, and contact URL.
- Basic normalization, validation, scoring, and OpenAI Responses API enrichment.
- CSV export for job leads.
- Docker Compose stack for API + worker + Postgres + Redis.

## Quickstart

```bash
cd leadgen-service
cp .env.example .env
docker compose up --build
```

API docs: <http://localhost:8000/docs>

## Running locally without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='postgresql+psycopg://postgres:postgres@localhost:5432/leadgen'
export REDIS_URL='redis://localhost:6379/0'
uvicorn app.main:app --reload
```

Worker:

```bash
celery -A app.workers.queue:celery_app worker --loglevel=info
```

## API Endpoints

- `GET /health`
- `POST /jobs`
- `GET /jobs/{job_id}`
- `GET /jobs/{job_id}/leads`
- `POST /jobs/{job_id}/export`
- `GET /exports/{export_id}`

## Safety and compliance notes

- Discovery uses a placeholder adapter (`SourceDiscoveryService`) and should be replaced with explicit permitted APIs only.
- URL fetches are validated through SSRF controls that block localhost/private/internal targets.
- Every lead stores `source_url` and `extraction_method` provenance fields.

## Tests

```bash
pytest
```
