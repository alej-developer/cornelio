"""
FastAPI dependency injection providers.

Centralizes service resolution so that endpoint handlers depend on
abstractions (LLMServiceBase, VectorStoreBase, DocumentParserBase)
rather than concrete implementations.
"""

from fastapi import Request

from app.services.base import DocumentParserBase, LLMServiceBase, VectorStoreBase
from app.services.document_parser import DocumentParser
from app.services.mlx_service import MLXService
from app.services.rag_engine import RAGEngine


async def get_mlx_service(request: Request) -> LLMServiceBase:
    """Resolve the LLM service from application state."""
    return request.app.state.mlx_service  # type: ignore[no-any-return]


async def get_rag_engine(request: Request) -> VectorStoreBase:
    """Resolve the RAG engine from application state."""
    return request.app.state.rag_engine  # type: ignore[no-any-return]


async def get_document_parser(request: Request) -> DocumentParserBase:
    """Resolve the document parser from application state."""
    return request.app.state.document_parser  # type: ignore[no-any-return]
