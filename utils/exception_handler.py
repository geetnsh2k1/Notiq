import logging
from typing import Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from exception.app_exception import AppException
from schema.base import ErrorResponse
from utils.parser import parse_validation_errors


logger = logging.getLogger(__name__)


def generate_error_response(
        status_code: int,
        error_code: int,
        message: str,
        error: Any = None
):
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            ErrorResponse(
                status_code=error_code,
                message=message,
                error=jsonable_encoder(error)
            )
        )
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail}")
    return generate_error_response(
        status_code=exc.status_code,
        error_code=exc.status_code,
        message="HTTP Exception",
        error=exc.detail
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("ValidationError encountered", exc_info=exc)

    errors = parse_validation_errors(exc.errors())

    return generate_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation Error",
        error=errors
    )


async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc}")
    return generate_error_response(
        status_code=exc.status_code,
        error_code=exc.error_code,
        message=exc.error_message,
        error=exc.error
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled Exception")
    return generate_error_response(
        status_code=500,
        error_code=500,
        message="Internal Server Error",
        error=str(exc)
    )
