from app.services.extractor import ExtractorService


def test_extractor_finds_contact_fields() -> None:
    html = """
    <html><head><title>ACME Plumbing</title></head>
    <body>
      Call us at (415) 555-1212 or email hello@acme.test
      <a href='/contact'>Contact</a>
    </body></html>
    """
    result = ExtractorService().extract("https://acme.test", html)
    assert result.business_name == "ACME Plumbing"
    assert result.email == "hello@acme.test"
    assert "415" in (result.phone or "")
    assert result.contact_page_url == "https://acme.test/contact"
