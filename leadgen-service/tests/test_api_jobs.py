from fastapi.testclient import TestClient

from app.main import app


def test_create_job() -> None:
    client = TestClient(app)
    payload = {"niche": "plumber", "geography": "Austin, TX", "keywords": ["emergency"]}
    response = client.post("/jobs", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["niche"] == "plumber"
    assert body["geography"] == "Austin, TX"
