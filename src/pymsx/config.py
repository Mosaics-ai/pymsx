"""Application wide configuration."""
import os
import tempfile
from dataclasses import dataclass
from typing import Optional

import dataconf

env_prefix = "MSX_"


@dataclass
class Configuration:
    """Aggregate app configuration."""

    org_id: Optional[str]
    email: Optional[str]
    password: Optional[str]
    token: Optional[str]

    temp_dir: str

    base_url: str

    org_header: str


configuration_defaults = {
    "temp_dir": tempfile.gettempdir(),
    "base_url": "https://api.mosaics.ai",
    "org_header": "X-Org-Id",
    "email": os.getenv("MSX_EMAIL"),
    "password": os.getenv("MSX_PASSWORD"),
}


def app_config(overrides: Optional[dict] = None):
    """Runtime application config."""
    return (
        dataconf.multi.dict(configuration_defaults)
        .env(env_prefix)
        .dict(overrides or {})
        .on(Configuration)
    )
