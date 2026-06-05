"""
Direct MLX inference endpoint (non-RAG).

POST /api/v1/inference/generate

Sends a prompt directly to the MLX model without retrieval augmentation.
"""

import logging

from fastapi import APIRouter, Depends

from app.schemas.inference import (
    ErrorResponse,
    InferenceRequest,
    InferenceResponse,
)
from app.services.base import LLMServiceBase
from app.services.dependencies import get_mlx_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/generate",
    response_model=InferenceResponse,
    responses={
        503: {"model": ErrorResponse, "description": "Model unavailable"},
    },
    summary="Generate text via direct MLX inference",
)
async def generate_text(
    request: InferenceRequest,
    llm: LLMServiceBase = Depends(get_mlx_service),
) -> InferenceResponse:
    """
    Generate text using the loaded MLX model without RAG context.

    If the model is not loaded, returns a degraded-mode response.
    """
    if not llm.is_loaded():
        return InferenceResponse(
            text=(
                "The MLX inference model is not currently loaded. "
                "Configure MLX_MODEL_PATH in the environment to enable generation."
            ),
            model="none",
            tokens_generated=0,
            latency_ms=0.0,
        )

    result = await llm.generate(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )

    return InferenceResponse(
        text=result.text,
        model=result.model_name,
        tokens_generated=result.tokens_generated,
        latency_ms=result.latency_ms,
    )
