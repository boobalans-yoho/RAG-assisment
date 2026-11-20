
from app.main import app, verify_api_key
from fastapi.testclient import TestClient


client = TestClient(app)


def test_unanswerable_question_fallback():
    app.dependency_overrides[verify_api_key] = lambda: True

    try:
        response = client.post(
            "/ask",
            json={
                "question": "What is the company office location on Mars?"
            }
        )

        assert response.status_code == 200
        assert response.json()["fallback"] is True
    finally:
        app.dependency_overrides.clear()


def test_empty_question():
    app.dependency_overrides[verify_api_key] = lambda: True

    try:
        response = client.post(
            "/ask",
            json={"question": ""}
        )

        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()
