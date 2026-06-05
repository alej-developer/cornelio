"""
Pruebas de humo para endpoints de infraestructura and API route availability.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Verifica que la prueba de liveness devuelva 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness_check() -> None:
    """Verifica que la prueba de readiness devuelva el estado estructurado."""
    response = client.get("/readiness")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "mlx_model_loaded" in data
    assert "vector_store_ready" in data


def test_inference_endpoint_exists() -> None:
    """Verifica que el endpoint de inferencia esté montado and accepts POST."""
    response = client.post(
        "/api/v1/inference/generate",
        json={"prompt": "test prompt"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "model" in data


def test_query_endpoint_exists() -> None:
    """Verifica que el endpoint de consulta RAG esté montado and accepts POST."""
    response = client.post(
        "/api/v1/query",
        json={"query": "test query"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data


def test_reports_endpoint_exists() -> None:
    """Verifica que el endpoint de reportes esté montado."""
    response = client.get("/api/v1/reports/generate")
    assert response.status_code == 200
    data = response.json()
    assert "report_id" in data
    assert "title" in data
    assert "sections" in data


def test_error_responses_are_sanitized() -> None:
    """Verifica que los errores no expongan detalles del servidor."""
    response = client.post(
        "/api/v1/inference/generate",
        json={},  # Falta campo requerido
    )
    assert response.status_code == 422
    data = response.json()
    # Los errores de validación de FastAPI no deben contener trazas de pila
    assert "traceback" not in str(data).lower()
