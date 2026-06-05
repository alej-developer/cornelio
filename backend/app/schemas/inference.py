"""
Pydantic schemas for all API request and response contracts.

All schemas enforce strict validation boundaries. No server-internal
fields are included in response models.
"""

from datetime import datetime

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# [ES] Endpoints de documentos / [EN] Document endpoints
# ---------------------------------------------------------------------------

class DocumentUploadResponse(BaseModel):
    """Response returned after a successful document upload and indexing."""

    document_id: str
    filename: str
    chunks_created: int
    status: str


class DocumentMetadata(BaseModel):
    """Metadata for a single indexed document."""

    document_id: str
    filename: str
    chunk_count: int
    indexed_at: str


# ---------------------------------------------------------------------------
# [ES] Endpoints de consultas / [EN] Query endpoints
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    """Input schema for the RAG query endpoint."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=4096,
        description="Natural language query against the document corpus.",
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of source documents to retrieve.",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature for the language model.",
    )
    max_tokens: int = Field(
        default=512,
        ge=1,
        le=4096,
        description="Maximum tokens in the generated response.",
    )


class SourceDocument(BaseModel):
    """A single source chunk returned with a query response."""

    content: str
    filename: str
    relevance_score: float


class QueryResponse(BaseModel):
    """Response from the RAG query pipeline."""

    answer: str
    sources: list[SourceDocument]
    model: str
    latency_ms: float


# ---------------------------------------------------------------------------
# [ES] Endpoints de informes / [EN] Report endpoints
# ---------------------------------------------------------------------------

class ReportSection(BaseModel):
    """A single section within a generated report."""

    heading: str
    body: str


class ReportResponse(BaseModel):
    """Structured report generated from indexed documents."""

    report_id: str
    title: str
    summary: str
    sections: list[ReportSection]
    document_count: int
    generated_at: str


# ---------------------------------------------------------------------------
# [ES] Endpoints de inferencia (existentes, consolidados aquí) / [EN] Inference endpoints (existing, consolidated here)
# ---------------------------------------------------------------------------

class InferenceRequest(BaseModel):
    """Direct inference request (non-RAG)."""

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=8192,
        description="Input prompt for the language model.",
    )
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class InferenceResponse(BaseModel):
    """Response from direct model inference."""

    text: str
    model: str
    tokens_generated: int
    latency_ms: float


# ---------------------------------------------------------------------------
# [ES] Respuesta de error (para documentación OpenAPI) / [EN] Error response (for OpenAPI documentation)
# ---------------------------------------------------------------------------

class ErrorResponse(BaseModel):
    """Standard error response envelope."""

    error: str
