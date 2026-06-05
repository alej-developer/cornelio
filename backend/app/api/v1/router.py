"""
API v1 router aggregation.

All versioned endpoint routers are mounted here.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import documents, inference, query, reports

api_router = APIRouter()

api_router.include_router(
    inference.router,
    prefix="/inference",
    tags=["inference"],
)

api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["documents"],
)

api_router.include_router(
    query.router,
    prefix="/query",
    tags=["query"],
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports"],
)
