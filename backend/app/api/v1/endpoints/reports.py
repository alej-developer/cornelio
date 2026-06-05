"""
Report generation endpoint.

GET /api/v1/reports/generate

Generates a structured summary report of all indexed documents
using the MLX model. Useful for automated briefing generation.
"""

import logging
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.core.exceptions import ReportGenerationError
from app.schemas.inference import (
    ErrorResponse,
    ReportResponse,
    ReportSection,
)
from app.services.base import LLMServiceBase, VectorStoreBase
from app.services.dependencies import get_mlx_service, get_rag_engine

logger = logging.getLogger(__name__)

router = APIRouter()

_REPORT_PROMPT_TEMPLATE: str = """You are a corporate reporting assistant. Generate a structured executive report based on the following document excerpts from the company knowledge base.

The report must include:
1. An executive summary
2. Key findings organized by topic
3. Actionable recommendations

Document excerpts:
{context}

Generate the report now. Use clear section headings."""


@router.get(
    "/generate",
    response_model=ReportResponse,
    responses={
        503: {"model": ErrorResponse, "description": "Model unavailable"},
        500: {"model": ErrorResponse, "description": "Generation error"},
    },
    summary="Generate an automated report from indexed documents",
)
async def generate_report(
    llm: LLMServiceBase = Depends(get_mlx_service),
    rag: VectorStoreBase = Depends(get_rag_engine),
) -> ReportResponse:
    """
    Generate a structured report summarizing all indexed corporate documents.

    Retrieves a representative sample of document chunks, then uses the
    MLX model to produce an executive-style report with sections.
    """
    start_time = time.perf_counter()

    # Gather document statistics
    try:
        doc_count = await rag.get_document_count()
        doc_ids = await rag.get_all_document_ids()
    except Exception as exc:
        logger.error("Failed to retrieve document stats: %s", str(exc))
        raise ReportGenerationError(
            internal_detail=f"Document stats retrieval failure: {exc}"
        ) from exc

    if doc_count == 0:
        return ReportResponse(
            report_id=uuid.uuid4().hex[:12],
            title="Corporate Knowledge Base Report",
            summary="No documents are currently indexed in the knowledge base.",
            sections=[
                ReportSection(
                    heading="Status",
                    body=(
                        "The document corpus is empty. Upload documents via "
                        "POST /api/v1/documents/upload to populate the knowledge base."
                    ),
                )
            ],
            document_count=0,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    # Retrieve a broad sample of chunks for the report
    try:
        sample_query = "summary overview key findings important information"
        sample_results = await rag.search(query=sample_query, k=15)
    except Exception as exc:
        logger.error("Failed to sample documents for report: %s", str(exc))
        raise ReportGenerationError(
            internal_detail=f"Document sampling failure: {exc}"
        ) from exc

    # Build context from sampled chunks
    context_block = "\n\n---\n\n".join(
        f"[Source: {r.source_filename}]\n{r.content}"
        for r in sample_results
    )

    # Generate report using LLM (or produce a metadata-only report)
    if not llm.is_loaded():
        sections = _build_metadata_sections(doc_ids, sample_results)
        return ReportResponse(
            report_id=uuid.uuid4().hex[:12],
            title="Corporate Knowledge Base Report (Metadata Only)",
            summary=(
                f"Automated report based on {doc_count} indexed chunks "
                f"across {len(doc_ids)} documents. "
                f"MLX model not loaded — showing metadata summary only."
            ),
            sections=sections,
            document_count=len(doc_ids),
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    try:
        prompt = _REPORT_PROMPT_TEMPLATE.format(context=context_block)
        result = await llm.generate(
            prompt=prompt,
            max_tokens=2048,
            temperature=0.4,
        )
    except Exception as exc:
        logger.error("Report generation LLM call failed: %s", str(exc))
        raise ReportGenerationError(
            internal_detail=f"LLM generation failure during report: {exc}"
        ) from exc

    # Parse generated text into sections
    sections = _parse_report_sections(result.text)

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    logger.info("Report generated in %.1f ms.", elapsed_ms)

    return ReportResponse(
        report_id=uuid.uuid4().hex[:12],
        title="Corporate Knowledge Base Report",
        summary=f"Automated report generated from {len(doc_ids)} documents.",
        sections=sections,
        document_count=len(doc_ids),
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def _build_metadata_sections(
    doc_ids: list[str],
    results: list,
) -> list[ReportSection]:
    """Build report sections from metadata when the LLM is unavailable."""
    sections: list[ReportSection] = []

    # Document inventory
    filenames: set[str] = set()
    for r in results:
        filenames.add(r.source_filename)

    sections.append(
        ReportSection(
            heading="Document Inventory",
            body=(
                f"Total indexed documents: {len(doc_ids)}\n"
                f"Unique source files: {', '.join(sorted(filenames)) or 'N/A'}"
            ),
        )
    )

    # Sample excerpts
    if results:
        excerpt_lines = []
        for i, r in enumerate(results[:5]):
            excerpt_lines.append(
                f"{i + 1}. [{r.source_filename}] {r.content[:200]}..."
            )
        sections.append(
            ReportSection(
                heading="Sample Excerpts",
                body="\n".join(excerpt_lines),
            )
        )

    return sections


def _parse_report_sections(text: str) -> list[ReportSection]:
    """
    Parse LLM-generated text into structured report sections.

    Splits on lines that appear to be headings (lines starting with #
    or lines in all-caps followed by content).
    """
    sections: list[ReportSection] = []
    current_heading: str = "Overview"
    current_body_lines: list[str] = []

    for line in text.split("\n"):
        stripped = line.strip()

        is_heading = (
            stripped.startswith("#")
            or (stripped.isupper() and len(stripped) > 3 and len(stripped) < 100)
            or stripped.endswith(":")
            and len(stripped) < 80
            and not any(c.islower() for c in stripped[:-1])
        )

        if is_heading and stripped:
            # Save previous section
            if current_body_lines:
                sections.append(
                    ReportSection(
                        heading=current_heading,
                        body="\n".join(current_body_lines).strip(),
                    )
                )
            current_heading = stripped.lstrip("# ").rstrip(":")
            current_body_lines = []
        else:
            current_body_lines.append(line)

    # Append final section
    if current_body_lines:
        sections.append(
            ReportSection(
                heading=current_heading,
                body="\n".join(current_body_lines).strip(),
            )
        )

    return sections if sections else [
        ReportSection(heading="Report", body=text.strip())
    ]
