from app.models.lead import Lead


class ScorerService:
    def score(self, lead: Lead) -> Lead:
        score = 0.0
        if lead.email:
            score += 45
        if lead.phone:
            score += 35
        if lead.contact_page_url:
            score += 10
        if lead.business_name:
            score += 10
        lead.lead_score = min(score, 100.0)
        return lead
