from typing import Any, Union
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """
    Base class for all API responses.

    Attributes:
        status_code (int): HTTP status code representing the result of the request.
        message (str): Human-readable message describing the result.
    """
    status_code: int = Field(..., description="HTTP status code representing the result of the request.")
    message: str = Field(..., description="Human-readable message describing the result.")


class Response(BaseResponse):
    """
    Generic success response wrapper.

    Attributes:
        data (Any, optional): The actual payload of the response, which can be any type or None.
    """
    data: Union[None, Any] = Field(None, description="Payload data of the response, if any.")


class ErrorResponse(BaseResponse):
    """
    Generic error response wrapper.

    Attributes:
        error (Any, optional): Additional error information, which can be any type or None.
    """
    error: Union[None, Any] = Field(None, description="Detailed error information, if available.")
