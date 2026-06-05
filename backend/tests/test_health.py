"""
Smoke tests for the health endpoint and API structure.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Verify the liveness probe returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_inference_endpoint_exists() -> None:
    """Verify the inference endpoint is mounted and accepts POST."""
    response = client.post(
        "/api/v1/inference/generate",
        json={"prompt": "test prompt"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "model" in data
