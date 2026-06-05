import pytest
from unittest.mock import AsyncMock, patch
from app.services.mlx_service import MLXService
from app.services.rag_engine import RAGEngine
from app.core.config import settings

@pytest.mark.asyncio
async def test_mlx_service_initialization():
    """Verify that MLXService initializes and respects safety parameters."""
    with patch("app.services.mlx_service.load") as mock_load:
        mock_load.return_value = ("mock_model", "mock_tokenizer")
        service = MLXService()
        await service.initialize()
        
        # Verify model loading was attempted using the safe local path from config
        mock_load.assert_called_once_with(settings.MLX_MODEL_PATH)
        assert service.is_ready is True

@pytest.mark.asyncio
async def test_rag_engine_initialization():
    """Verify that RAGEngine initializes with safe telemetry settings."""
    with patch("app.services.rag_engine.chromadb.PersistentClient") as mock_chroma:
        engine = RAGEngine()
        await engine.initialize()
        
        # Verify that telemetry is strictly disabled for security/privacy
        mock_chroma.assert_called_once()
        call_settings = mock_chroma.call_args[1].get('settings')
        assert call_settings.anonymized_telemetry is False
        assert engine.is_ready is True
