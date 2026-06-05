"""
MLX inference endpoints.

Provides text generation via Apple MLX models.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class InferenceRequest(BaseModel):
    """Schema for inference input."""

    prompt: str = Field(..., min_length=1, max_length=8192, description="Input prompt text.")
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class InferenceResponse(BaseModel):
    """Schema for inference output."""

    text: str
    model: str
    tokens_generated: int
    latency_ms: float


@router.post("/generate", response_model=InferenceResponse)
async def generate_text(request: InferenceRequest) -> InferenceResponse:
    """
    Generate text using the loaded MLX model.

    This is a placeholder that will be replaced with actual MLX inference logic.
    """
    return InferenceResponse(
        text="[MLX model not loaded — placeholder response]",
        model="none",
        tokens_generated=0,
        latency_ms=0.0,
    )
