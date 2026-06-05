"""
Document parser service implementation.

Handles extraction of raw text from PDF and TXT files.
Follows the Single Responsibility Principle: this module only parses,
it does not chunk, vectorize, or store.
"""

import io
import logging

from app.core.exceptions import DocumentProcessingError, UnsupportedFileTypeError
from app.services.base import DocumentParserBase

logger = logging.getLogger(__name__)

_SUPPORTED_MIME_TYPES: set[str] = {
    "application/pdf",
    "text/plain",
}


class DocumentParser(DocumentParserBase):
    """Concrete parser for PDF and plain-text documents."""

    def supported_types(self) -> set[str]:
        return _SUPPORTED_MIME_TYPES.copy()

    async def parse(
        self,
        content: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        """
        Extract text from raw file bytes.

        Delegates to format-specific private methods based on MIME type.
        """
        normalized_type = content_type.lower().strip()

        if normalized_type not in _SUPPORTED_MIME_TYPES:
            raise UnsupportedFileTypeError(content_type)

        try:
            if normalized_type == "application/pdf":
                return self._parse_pdf(content, filename)
            return self._parse_text(content, filename)
        except UnsupportedFileTypeError:
            raise
        except Exception as exc:
            logger.error(
                "Failed to parse document '%s' (type=%s): %s",
                filename,
                content_type,
                str(exc),
            )
            raise DocumentProcessingError(
                internal_detail=f"Parse failure for '{filename}': {exc}"
            ) from exc

    def _parse_pdf(self, content: bytes, filename: str) -> str:
        """Extract text from all pages of a PDF document."""
        try:
            from PyPDF2 import PdfReader
        except ImportError as exc:
            raise DocumentProcessingError(
                internal_detail="PyPDF2 is not installed."
            ) from exc

        reader = PdfReader(io.BytesIO(content))
        pages: list[str] = []

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append(text.strip())
            else:
                logger.warning(
                    "Empty text extraction on page %d of '%s'.",
                    page_num + 1,
                    filename,
                )

        if not pages:
            raise DocumentProcessingError(
                internal_detail=f"No extractable text found in PDF '{filename}'."
            )

        return "\n\n".join(pages)

    def _parse_text(self, content: bytes, filename: str) -> str:
        """Decode plain text with encoding fallback."""
        for encoding in ("utf-8", "latin-1", "cp1252"):
            try:
                text = content.decode(encoding)
                if text.strip():
                    return text.strip()
            except (UnicodeDecodeError, ValueError):
                continue

        raise DocumentProcessingError(
            internal_detail=f"Unable to decode text file '{filename}' with any supported encoding."
        )
