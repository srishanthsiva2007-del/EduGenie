from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    r = client.get('/')
    assert r.status_code == 200
    assert 'EduGenie' in r.text

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'

def test_explain_unavailable_returns_friendly_message(monkeypatch):
    def raise_unavailable(_question):
        raise RuntimeError("503 UNAVAILABLE: This model is currently experiencing high demand")

    monkeypatch.setattr("main.explain_concept", raise_unavailable)
    r = client.post('/explain', json={"question": "What is gravity?"})

    assert r.status_code == 503
    assert r.json()["detail"] == "The AI service is experiencing high demand. Please try again later."
