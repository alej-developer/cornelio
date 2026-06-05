"""
Document upload endpoint.

POST /api/v1/documents/upload

Accepts PDF and TXT files, parses content, chunks text,
and indexes into the vector store for RAG retrieval.
"""

import logging
import uuid

from fastapi import APIRouter, Depends, UploadFile, status

from app.core.config import settings
from app.core.exceptions import (
    DocumentProcessingError,
    FileSizeExceededError,
    UnsupportedFileTypeError,
)
from app.schemas.inference import DocumentUploadResponse, ErrorResponse
from app.services.base import DocumentParserBase, VectorStoreBase
from app.services.dependencies import get_document_parser, get_rag_engine
from app.services.rag_engine import create_document_chunks

logger = logging.getLogger(__name__)

router = APIRouter()

_ALLOWED_CONTENT_TYPES: set[str] = {"application/pdf", "text/plain"}


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        413: {"model": ErrorResponse, "description": "File too large"},
        415: {"model": ErrorResponse, "description": "Unsupported file type"},
        422: {"model": ErrorResponse, "description": "Processing error"},
    },
    summary="Upload and index a document",
)
async def upload_document(
    file: UploadFile,
    parser: DocumentParserBase = Depends(get_document_parser),
    rag: VectorStoreBase = Depends(get_rag_engine),
) -> DocumentUploadResponse:
    """
    Upload a PDF or TXT document for indexing into the RAG pipeline.

    The file is parsed, split into chunks, vectorized, and stored locally
    in the ChromaDB vector store. No data is transmitted externally.
    """
    # Validate content type
    content_type = file.content_type or ""
    if content_type not in _ALLOWED_CONTENT_TYPES:
        raise UnsupportedFileTypeError(content_type)

    # Read and validate file size
    content = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise FileSizeExceededError(settings.MAX_UPLOAD_SIZE_MB)

    filename = file.filename or "unnamed_document"

    # Parse raw text
    raw_text = await parser.parse(content, filename, content_type)

    if not raw_text.strip():
        raise DocumentProcessingError(
            internal_detail=f"No text content extracted from '{filename}'."
        )

    # Chunk and index
    document_id = uuid.uuid4().hex[:12]
    chunks = create_document_chunks(
        text=raw_text,
        filename=filename,
        document_id=document_id,
    )

    indexed_count = await rag.add_documents(chunks)

    logger.info(
        "Document '%s' indexed: id=%s, chunks=%d",
        filename,
        document_id,
        indexed_count,
    )

    return DocumentUploadResponse(
        document_id=document_id,
        filename=filename,
        chunks_created=indexed_count,
        status="indexed",
    )
