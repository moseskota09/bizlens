from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class SourceJob(Base):
    __tablename__ = "source_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    niche: Mapped[str] = mapped_column(String(255), nullable=False)
    geography: Mapped[str] = mapped_column(String(255), nullable=False)
    keywords_json: Mapped[str] = mapped_column(Text, default="[]")
    status: Mapped[str] = mapped_column(String(32), default="pending")
    total_candidates: Mapped[int] = mapped_column(Integer, default=0)
    total_extracted: Mapped[int] = mapped_column(Integer, default=0)
    total_valid: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    leads = relationship("Lead", back_populates="job", cascade="all, delete-orphan")
