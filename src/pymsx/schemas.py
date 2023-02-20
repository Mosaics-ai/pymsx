"""Schemas for api responses and requests."""
from dataclasses import asdict, dataclass


@dataclass
class Credentials:
    """Credential model for requesting token."""

    email: str
    password: str

    dict = asdict


@dataclass
class TokenResponse:
    """Response when requesting api token."""

    token: str
    orgId: str

    dict = asdict


@dataclass
class ApiMessage:
    """Generic api response on certain routes."""

    message: str

    dict = asdict


@dataclass
class ApiError:
    """Generic api error response."""

    error: str

    dict = asdict


@dataclass
class HealthStatus:
    """Schema for remote server health status."""

    build: str
    sid: int
    status: str
    time: str

    dict = asdict
