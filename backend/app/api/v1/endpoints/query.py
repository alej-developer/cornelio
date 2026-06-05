"""
RAG query endpoint.

POST /api/v1/query

Receives a natural language query, retrieves relevant document chunks
from the vector store, constructs an augmented prompt, and generates
a response using the MLX model.
"""

import logging
import time

from fastapi import APIRouter, Depends

from app.core.exceptions import ModelNotLoadedError, QueryError
from app.schemas.inference import (
    ErrorResponse,
    QueryRequest,
    QueryResponse,
    SourceDocument,
)
from app.services.base import LLMServiceBase, VectorStoreBase
from app.services.dependencies import get_mlx_service, get_rag_engine

logger = logging.getLogger(__name__)

router = APIRouter()

_RAG_PROMPT_TEMPLATE: str = """You are a corporate assistant. Answer the question based strictly on the provided context. If the context does not contain enough information, state that clearly.

Context:
{context}

Question: {question}

Answer:"""


@router.post(
    "",
    response_model=QueryResponse,
    responses={
        503: {"model": ErrorResponse, "description": "Model unavailable"},
        500: {"model": ErrorResponse, "description": "Query processing error"},
    },
    summary="Query documents using RAG",
)
async def query_documents(
    request: QueryRequest,
    llm: LLMServiceBase = Depends(get_mlx_service),
    rag: VectorStoreBase = Depends(get_rag_engine),
) -> QueryResponse:
    """
    Execute a retrieval-augmented query against indexed documents.

    1. Retrieves the top-k relevant chunks from the vector store.
    2. Constructs a context-augmented prompt.
    3. Generates a response using the local MLX model.
    """
    start_time = time.perf_counter()

    # Step 1: Retrieve relevant context
    try:
        search_results = await rag.search(
            query=request.query,
            k=request.max_results,
        )
    except Exception as exc:
        logger.error("RAG search failed for query: %s", str(exc))
        raise QueryError(
            internal_detail=f"Vector search failure: {exc}"
        ) from exc

    # Build source documents for response
    sources = [
        SourceDocument(
            content=result.content[:500],  # Truncate for response payload
            filename=result.source_filename,
            relevance_score=result.score,
        )
        for result in search_results
    ]

    # Step 2: Construct augmented prompt
    if search_results:
        context_block = "\n\n---\n\n".join(
            f"[Source: {r.source_filename}]\n{r.content}"
            for r in search_results
        )
        augmented_prompt = _RAG_PROMPT_TEMPLATE.format(
            context=context_block,
            question=request.query,
        )
    else:
        augmented_prompt = (
            f"No documents are currently indexed. "
            f"Answer the following question to the best of your ability:\n\n"
            f"{request.query}"
        )

    # Step 3: Generate response
    if not llm.is_loaded():
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return QueryResponse(
            answer=(
                "The inference model is not currently loaded. "
                "Document retrieval completed successfully. "
                "Please configure MLX_MODEL_PATH to enable generation."
            ),
            sources=sources,
            model="none",
            latency_ms=round(elapsed_ms, 2),
        )

    try:
        result = await llm.generate(
            prompt=augmented_prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
    except ModelNotLoadedError:
        raise
    except Exception as exc:
        logger.error("LLM generation failed: %s", str(exc))
        raise QueryError(
            internal_detail=f"LLM generation failure: {exc}"
        ) from exc

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return QueryResponse(
        answer=result.text,
        sources=sources,
        model=result.model_name,
        latency_ms=round(elapsed_ms, 2),
    )
