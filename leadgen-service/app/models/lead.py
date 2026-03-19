from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("source_jobs.id", ondelete="CASCADE"), index=True)
    business_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website: Mapped[str] = mapped_column(String(2048), nullable=False)
    root_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_page_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    decision_maker_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    decision_maker_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    personalization_line: Mapped[str | None] = mapped_column(Text, nullable=True)
    lead_score: Mapped[float] = mapped_column(Float, default=0.0)
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    extraction_method: Mapped[str] = mapped_column(String(64), default="http")
    is_valid: Mapped[bool] = mapped_column(Boolean, default=False)
    validation_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = relationship("SourceJob", back_populates="leads")
