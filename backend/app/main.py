"""
FastAPI application entrypoint.

Configures CORS, lifespan events (service initialization and teardown),
exception handlers, and mounts the versioned API router.
"""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.api.v1.router import api_router
from app.services.mlx_service import MLXService
from app.services.rag_engine import RAGEngine
from app.services.document_parser import DocumentParser

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


# ---------------------------------------------------------------------------
# Application lifespan — service initialization and teardown
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage the application lifecycle.

    Startup: initialize MLX model, RAG engine, and document parser.
    Shutdown: release model resources and persist vector store state.
    """
    # --- Startup ---
    logger.info("Initializing services...")

    # Document parser (stateless, no async init needed)
    app.state.document_parser = DocumentParser()

    # RAG engine (ChromaDB)
    rag_engine = RAGEngine(settings)
    try:
        await rag_engine.initialize()
    except Exception:
        logger.warning(
            "ChromaDB initialization failed. "
            "Document indexing and retrieval will be unavailable."
        )
    app.state.rag_engine = rag_engine

    # MLX model (may not be available on non-Apple-Silicon platforms)
    mlx_service = MLXService(settings)
    try:
        await mlx_service.load_model()
    except Exception:
        logger.warning(
            "MLX model loading failed. "
            "The API will operate in retrieval-only mode."
        )
    app.state.mlx_service = mlx_service

    logger.info("All services initialized. Application is ready.")

    yield

    # --- Shutdown ---
    logger.info("Shutting down services...")
    await mlx_service.unload_model()
    logger.info("Shutdown complete.")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Cornelio API — Local MLX inference and RAG pipeline.",
    docs_url="/docs" if settings.APP_DEBUG else None,
    redoc_url="/redoc" if settings.APP_DEBUG else None,
    lifespan=lifespan,
)

# Register sanitized exception handlers (no server internals exposed)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Infrastructure endpoints
# ---------------------------------------------------------------------------

@app.get("/health", tags=["infrastructure"])
async def health_check() -> dict[str, str]:
    """Liveness probe for orchestrators and load balancers."""
    return {"status": "healthy"}


@app.get("/readiness", tags=["infrastructure"])
async def readiness_check() -> dict[str, str | bool]:
    """
    Readiness probe indicating whether all services are operational.

    Returns degraded status if any service is unavailable.
    """
    mlx_ready = hasattr(app.state, "mlx_service") and app.state.mlx_service.is_loaded()
    rag_ready = hasattr(app.state, "rag_engine") and app.state.rag_engine._initialized

    overall = "ready" if (mlx_ready and rag_ready) else "degraded"

    return {
        "status": overall,
        "mlx_model_loaded": mlx_ready,
        "vector_store_ready": rag_ready,
    }
