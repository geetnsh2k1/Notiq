import logging
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id  # Store for later use
        user_id = request.headers.get("X-User-ID", "anonymous")

        start_time = time.time()

        response = await call_next(request)

        duration = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"{request.method} {request.url.path} "
            f"completed_in={duration}ms status={response.status_code} "
            f"request_id={request_id} user_id={user_id}"
        )

        # Add request ID in response headers (optional)
        response.headers["X-Request-ID"] = request_id

        return response
