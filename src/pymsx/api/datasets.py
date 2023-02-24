"""Datasets Class used to access remote datasets and metadata.

Datasets represent remote data and their versions. Data is organized by `dataset name`
and versions. Versions are created automatically, and associating versions is done by
reusing existing `dataset names`.

For example, if uploading file `nlp_train.csv` today, the msx server will store that
dataset under the dataset name `nlp_train`. If I then another, newer file also named
`nlp_train.csv`, the msx server will automatically associate them, and store the second
dataset as `version 2`.

The same applies to dataframes, passed in with a name, instead of a file path.

Classes:
    Datasets
"""
import io
import logging
import pathlib
from typing import TYPE_CHECKING, Any, Callable, Optional

import pandas as pd
import requests
from requests_toolbelt.multipart.encoder import (
    MultipartEncoder,
    MultipartEncoderMonitor,
)

if TYPE_CHECKING:
    from pymsx.client import MsxClient


logger = logging.getLogger(__name__)


class Datasets:
    """
    Main class for managing datasets on remote msx servers.

    ...

    Args:
        client (:obj: `MsxClient`): the client used to perform remote api requests

    Attributes:
        client (:obj: `MsxClient`): the client used to perform remote api requests
    """

    def __init__(self, client: "MsxClient"):
        """Create a new Datasets class."""
        self.client = client

    def __get_df_size(self, df: pd.DataFrame):
        try:
            return df.memory_usage(index=True).sum()
        except Exception:
            # size is not essential
            return None

    def __get_mime_type(self, ext: str = ".csv"):
        if ext == ".csv":
            return "text/csv"
        elif ext == ".parquet":
            return "application/parquet"
        elif ext == ".json":
            return "application/parquet"
        else:
            return "text/plain"

    def __get_pd_read_func(self, ext: str = ".csv"):
        read_func = pd.read_csv
        if ext == ".csv":
            pass
        elif ext == ".parquet":
            read_func = pd.read_parquet
        elif ext == ".json":
            read_func = pd.read_json
        else:
            # must be unreachable
            pass
        return read_func

    def __convert_df_to_bytes(self, df: pd.DataFrame, ext: str = ".csv") -> io.BytesIO:
        if ext == ".csv":
            data = io.BytesIO(df.to_csv(index=False).encode("utf-8"))
        elif ext == ".parquet":
            data = io.BytesIO(df.to_parquet(index=False))
        elif ext == ".json":
            data = io.BytesIO(df.to_json(index=False).encode("utf-8"))
        else:
            # must be unreachable
            data = io.BytesIO(df.to_csv(index=False).encode("utf-8"))
        data.seek(0)
        return data

    def add(
        self,
        path_or_name: str,
        df: Optional[pd.DataFrame] = None,
        target: Optional[str] = None,
        store_s3: bool = False,
        df_read_args: Optional[dict[str, Any]] = None,
        callback: Optional[Callable[[MultipartEncoderMonitor], None]] = None,
        **kwargs,
    ):
        """
        Add a dataset to the connected msx server.

        If df is None, then first arg is used as `dataset name` otherwise it must be
        a path to a dataset (file on disk, or soon a location that pandas can parse,
        such as s3)

        Args:
            path_or_name (str): Either a dataset name (if df is provided), or the path
                to a file on disk.
            df (:ob: `pandas.DataFrame`): A pandas dataframe
            target (str, optional): The target (column) of the data that will be used
                when training. If no target is provided, then the last column will be
                used.
            store_s3 (bool, optional): Data can be stored in the isolated msx
                environment, or it can be stored in an accessible (secure) S3 bucket
                that every msx server includes.
            df_read_args (dict[str, Any], optional): If df is not defined, then
                optionally pass in pandas read_* kwargs.
            **kwargs: If kwargs are provided, they will be serialized to dict[str, str]
                and passed to the upload server as is. This is useful because it allows
                passing additional fields to any pipelines or triggers configured to
                run after upload

        Returns:
            {
                path: str,
                **kwargs
            }
        """
        filename = path_or_name

        # READ
        if df is None:
            # attempt reading path_or_name as path
            path = pathlib.Path(path_or_name)
            filename = path.name
            path_ext = path.suffix

            allowed_ext = self.client.config.allowed_read_exts

            if path_ext not in allowed_ext:
                raise ValueError(f"Could not read path type {path_ext}")

            if path_ext == "":
                raise ValueError("Path extension could not be determined.")

            # read path
            read_func = self.__get_pd_read_func(ext=path_ext)

            if df_read_args is not None:
                df = read_func(path_or_name, **df_read_args)
            else:
                df = read_func(path_or_name)

        # WRITE

        # for now using `.csv` for everything write related
        write_ext = ".csv"

        callback = callback or default_monitor

        target = target or "default"
        extra = {}
        if kwargs is not None:
            extra = {
                k: (str(v), io.BytesIO(bytes(str(v), "utf-8")), "text/plain")
                for k, v in kwargs.items()
            }

        filename = f"/s3/{filename}" if store_s3 else f"/datasets/{filename}"

        data = self.__convert_df_to_bytes(df, ext=write_ext)

        # stream = StreamingIterator(size, data)

        e = MultipartEncoder(
            fields={
                **extra,
                "file": (filename, data, self.__get_mime_type(write_ext)),
                "target": (target, io.BytesIO(bytes(target, "utf-8")), "text/plain"),
            }
        )
        m = MultipartEncoderMonitor(e, callback)

        url = f"{self.client.base_url}/upload"

        auth_headers = self.client.get_auth_headers()
        auth_headers = self.client.add_org_header(headers=auth_headers)

        res = requests.post(
            url, data=m, headers={**auth_headers, "Content-type": e.content_type}
        )

        return res.json()


def default_monitor(monitor: MultipartEncoderMonitor) -> None:
    """Monitor for MultipartEncodeMonitor."""
    logger.debug(f"Bytes read: {monitor.bytes_read}")
