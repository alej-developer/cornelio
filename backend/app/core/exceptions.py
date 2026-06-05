"""
Custom exception hierarchy and global exception handlers.

Design principle: all exceptions return sanitized, user-safe messages.
Internal details are logged server-side and never exposed to the client.
"""

import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for all application-level errors."""

    def __init__(
        self,
        message: str = "An internal error occurred.",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        internal_detail: str | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.internal_detail = internal_detail or message
        super().__init__(self.message)


class ModelNotLoadedError(AppException):
    """The MLX model is not loaded or unavailable."""

    def __init__(self, internal_detail: str | None = None) -> None:
        super().__init__(
            message="The inference service is temporarily unavailable.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            internal_detail=internal_detail or "MLX model not loaded.",
        )


class DocumentProcessingError(AppException):
    """Document parsing or vectorization failed."""

    def __init__(self, internal_detail: str | None = None) -> None:
        super().__init__(
            message="Failed to process the uploaded document.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            internal_detail=internal_detail or "Document processing pipeline failure.",
        )


class VectorStoreError(AppException):
    """The vector store encountered an operational error."""

    def __init__(self, internal_detail: str | None = None) -> None:
        super().__init__(
            message="The search service encountered an error.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            internal_detail=internal_detail or "Vector store operation failed.",
        )


class FileSizeExceededError(AppException):
    """Uploaded file exceeds the configured maximum size."""

    def __init__(self, max_size_mb: int) -> None:
        super().__init__(
            message=f"File size exceeds the maximum allowed limit of {max_size_mb} MB.",
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        )


class UnsupportedFileTypeError(AppException):
    """The uploaded file type is not among the accepted formats."""

    def __init__(self, content_type: str) -> None:
        super().__init__(
            message="The uploaded file type is not supported. Accepted formats: PDF, TXT.",
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            internal_detail=f"Rejected content type: {content_type}",
        )


class QueryError(AppException):
    """A query against the RAG pipeline failed."""

    def __init__(self, internal_detail: str | None = None) -> None:
        super().__init__(
            message="Unable to process the query at this time.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            internal_detail=internal_detail or "RAG query pipeline failure.",
        )


class ReportGenerationError(AppException):
    """Report generation failed."""

    def __init__(self, internal_detail: str | None = None) -> None:
        super().__init__(
            message="Unable to generate the report at this time.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            internal_detail=internal_detail or "Report generation pipeline failure.",
        )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers on the FastAPI instance.

    Ensures that no unhandled exception leaks internal state to the client.
    """

    @app.exception_handler(AppException)
    async def handle_app_exception(
        request: Request, exc: AppException
    ) -> JSONResponse:
        logger.error(
            "AppException [%d] %s | method=%s path=%s",
            exc.status_code,
            exc.internal_detail,
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message},
        )

    @app.exception_handler(Exception)
    async def handle_unhandled_exception(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.critical(
            "Unhandled exception: %s | method=%s path=%s",
            str(exc),
            request.method,
            request.url.path,
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "An unexpected error occurred. Please try again later."},
        )
