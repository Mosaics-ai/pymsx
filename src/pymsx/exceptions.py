"""Exceptions thrown by classes in pymsx."""
from typing import Optional

from pymsx.schemas import ApiError


class ApiResponseError(Exception):
    """Exception raised for api errors.

    Attributes:
        error: str - the error message if any
    """

    def __init__(self, error: Optional[ApiError] = None):
        """Raise api response error."""
        self.error = error.error if error is not None else "Unknown error"
        super().__init__(self.error)


class InvalidTokenError(Exception):
    """Exception raised when token invalid."""

    def __init__(self):
        """Raise invalid token error."""
        super().__init__("You are not authorized to make this request: Invalid token")
