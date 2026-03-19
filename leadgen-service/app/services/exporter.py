import csv
from pathlib import Path

from app.core.config import get_settings
from app.models.lead import Lead


class ExporterService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def export_csv(self, job_id: int, leads: list[Lead]) -> Path:
        output_path = self.settings.exports_dir / f"job_{job_id}.csv"
        fields = [
            "id",
            "business_name",
            "website",
            "email",
            "phone",
            "contact_page_url",
            "lead_score",
            "is_valid",
            "source_url",
        ]
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for lead in leads:
                writer.writerow({k: getattr(lead, k) for k in fields})
        return output_path
