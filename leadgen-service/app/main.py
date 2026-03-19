from fastapi import FastAPI

from app.api.routes.exports import router as exports_router
from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.core.config import get_settings
from app.core.database import engine
from app.core.logging import configure_logging
from app.models import Base

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(jobs_router)
app.include_router(exports_router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
