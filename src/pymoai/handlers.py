"""Simple handlers to manage responses from server.

Functions
    handle_response(res: requests.Response) -> Any | str | ApiError
    handle_unknown_response(msg: Optional[str] = None) -> ApiError
"""
import logging
from typing import Any, Optional, Union

import requests
from dacite import from_dict

from pymoai.schemas import ApiError

logger = logging.getLogger(__name__)


def handle_response(res: requests.Response) -> Union[str, Any, ApiError]:
    """Handle server responses."""
    if res.ok:
        try:
            return res.json()
        except requests.exceptions.JSONDecodeError:
            return res.text
    else:
        try:
            return ApiError(error=f"(Code: {res.status_code}): {res.reason}")
        except Exception:
            return ApiError(error="(Code: 0): unknown")


def handle_unknown_response(msg: Optional[str] = None) -> ApiError:
    """Hanlde unknown response types."""
    prefix = "Unknown response"
    message = prefix if msg is None else f"{prefix}: {msg}"
    return from_dict(data={"error": message}, data_class=ApiError)
