from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ask_endpoint(monkeypatch):
    def fake_answer(question: str) -> str:
        return "Azure Key Vault."

    monkeypatch.setattr("src.api.main.rag.answer", fake_answer)

    response = client.post(
        "/ask",
        json={"question": "Where should I store application passwords?"},
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "Azure Key Vault."}


def test_ask_rejects_missing_question():
    response = client.post("/ask", json={})

    assert response.status_code == 422