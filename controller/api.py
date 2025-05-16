import logging

from fastapi import APIRouter

from schema.base import Response


logger: logging.Logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(
    prefix="/api",
    tags=["Health Check"],
)

@router.get(
    path="/health",
    status_code=200,
    summary="Health check",
    description="Check the health of the API."
)
async def health_check() -> str:
    """
    Health check endpoint.
    """
    return "healthy"