from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_validation_rejects_empty_document_type():
    r = client.post("/generate", json={"document_type":"", "parties":"A", "terms":"B", "dates":"C"})
    assert r.status_code == 422
