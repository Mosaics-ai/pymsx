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

    # dataset specific
    temp_dir: str
    allowed_read_exts: list[str]
    min_stream_size: int

    base_url: str

    org_header: str


configuration_defaults = {
    "temp_dir": tempfile.gettempdir(),
    "base_url": "https://api.mosaics.ai",
    "org_header": "X-Org-Id",
    "email": os.getenv("MSX_EMAIL"),
    "password": os.getenv("MSX_PASSWORD"),
    "allowed_read_exts": [".csv", ".parquet", ".json"],
    "min_stream_size": 1024 * 1024 * 1024,
}


def app_config(overrides: Optional[dict] = None) -> Configuration:
    """Runtime application config."""
    config: Configuration = (
        dataconf.multi.dict(configuration_defaults)
        .env(env_prefix)
        .dict(overrides or {})
        .on(Configuration)
    )
    return config
