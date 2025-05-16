from pydantic import BaseModel, Field


class RequestValidationError(BaseModel):
    """
    Custom validation error object for field-level validation issues.

    Attributes:
        type (str): The type/category of validation error.
        field_name (str): The name of the field where validation failed.
        message (str): The validation error message.
    """
    type: str = Field(..., description="Type of validation error (e.g., value_error)")
    field_name: str = Field(..., description="Field name where the validation failed")
    message: str = Field(..., description="Details about the validation error")
