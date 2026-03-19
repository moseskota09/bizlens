from app.services.extractor import ExtractedFields
from app.services.normalizer import NormalizerService


def test_normalizer_phone_and_email() -> None:
    fields = ExtractedFields(
        business_name="Test Co",
        email="Sales@Example.COM",
        phone="(212) 555-0987",
        contact_page_url="https://example.com/contact",
        text_excerpt="",
    )
    lead = NormalizerService().normalize(
        job_id=1,
        website="https://example.com",
        source_url="https://source.example",
        fields=fields,
        method="http",
    )
    assert lead.email == "sales@example.com"
    assert lead.phone == "+12125550987"
    assert lead.root_domain == "example.com"
