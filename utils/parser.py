from typing import List, Any

from schema.request_validation_error import RequestValidationError

def parse_validation_errors(raw_errors: Any) -> List[RequestValidationError]:
    """
    Safely converts raw Pydantic validation errors into structured objects.
    
    Args:
        raw_errors (Any): Output from `RequestValidationError.errors()`

    Returns:
        List[RequestValidationError]: List of structured errors
    """
    structured_errors = []

    try:
        for err in raw_errors:
            loc = err.get("loc", [])
            if isinstance(loc, (list, tuple)):
                field = ".".join(map(str, loc))
            else:
                field = str(loc)

            structured_errors.append(
                RequestValidationError(
                    type=err.get("type", "unknown_error"),
                    field_name=field,
                    message=err.get("msg", "Unknown validation error")
                )
            )
    except Exception:
        structured_errors.append(
            RequestValidationError(
                type="internal_error",
                field_name="N/A",
                message="Failed to parse validation errors"
            )
        )

    return structured_errors
