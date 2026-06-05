"""
API v1 router aggregation.

All versioned endpoint routers are mounted here.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import inference

api_router = APIRouter()

api_router.include_router(
    inference.router,
    prefix="/inference",
    tags=["inference"],
)
