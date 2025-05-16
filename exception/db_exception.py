from typing import Any, Union

from exception.app_exception import AppException


class DBException(AppException):
    """
    Custom exception for database-related errors, extending AppException.

    Attributes:
        error_code (int): Application-specific code representing the DB error.
        error_message (str): Description of the database error.
        error (Any, optional): Detailed context (e.g., SQL error, trace info).
        status_code (int): HTTP status code associated with this error (default is 500).
    """

    def __init__(
        self,
        error_code: int,
        error_message: str,
        error: Union[Any, None] = None,
        status_code: int = 500
    ):
        """
        Initialize a DBException instance.

        Args:
            error_code (int): Unique identifier for the DB error.
            error_message (str): A human-readable explanation of the error.
            error (Any, optional): Additional context for debugging.
            status_code (int, optional): HTTP status code (default is 500).
        """
        super().__init__(
            error_code=error_code,
            error_message=error_message,
            error=error,
            status_code=status_code
        )
