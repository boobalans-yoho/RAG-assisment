
from fastapi.testclient import TestClient
from app.config import settings
from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_ask_without_api_key():
    response = client.post(
        "/ask",
        json={"question": "What is the leave policy?"}
    )
    assert response.status_code == 401


def test_ask_with_invalid_api_key():
    response = client.post(
        "/ask",
        headers={"X-API-Key": "wrong-key"},
        json={"question": "What is the leave policy?"}
    )
    assert response.status_code == 403


def test_ask_empty_question():
    response = client.post(
        "/ask",
        headers={"X-API-Key": settings.API_KEY},
        json={"question": ""}
    )

    assert response.status_code == 422
