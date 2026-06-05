import pytest
from unittest.mock import AsyncMock, patch
from app.services.mlx_service import MLXService
from app.services.rag_engine import RAGEngine
from app.core.config import settings

@pytest.mark.asyncio
async def test_mlx_service_initialization():
    """Verifica que MLXService se inicialice y respete la seguridad."""
    with patch("app.services.mlx_service.load") as mock_load:
        mock_load.return_value = ("mock_model", "mock_tokenizer")
        service = MLXService()
        await service.initialize()
        
        # Verifica el intento de carga del modelo usando la ruta local segura
        mock_load.assert_called_once_with(settings.MLX_MODEL_PATH)
        assert service.is_ready is True

@pytest.mark.asyncio
async def test_rag_engine_initialization():
    """Verifica que RAGEngine inicialice con configuraciones seguras."""
    with patch("app.services.rag_engine.chromadb.PersistentClient") as mock_chroma:
        engine = RAGEngine()
        await engine.initialize()
        
        # Verifica que la telemetría esté deshabilitada por seguridad
        mock_chroma.assert_called_once()
        call_settings = mock_chroma.call_args[1].get('settings')
        assert call_settings.anonymized_telemetry is False
        assert engine.is_ready is True
