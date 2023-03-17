"""Datasets Class used to access remote datasets and metadata.

Datasets represent remote data and their versions. Data is organized by `dataset name`
and versions. Versions are created automatically, and associating versions is done by
reusing existing `dataset names`.

For example, if uploading file `nlp_train.csv` today, the moai server will store that
dataset under the dataset name `nlp_train`. If I then another, newer file also named
`nlp_train.csv`, the moai server will automatically associate them, and store the second
dataset as `version 2`.

The same applies to dataframes, passed in with a name, instead of a file path.

Classes:
    Datasets
"""
import logging
from typing import TYPE_CHECKING, Any, Optional, Union

import requests

from pymoai import handlers
from pymoai.schemas import ApiError, CommandArgs

if TYPE_CHECKING:
    from pymoai.client import MoaiClient


logger = logging.getLogger(__name__)


class Commands:
    """
    Main class for issuing commands to remote moai servers.

    ...

    Args:
        client (:obj: `MoaiClient`): the client used to perform remote api requests

    Attributes:
        client (:obj: `MoaiClient`): the client used to perform remote api requests
    """

    def __init__(self, client: "MoaiClient"):
        """Create a new Commands class."""
        self.client = client

    def run(
        self, task: str, args: Optional[list[str]] = None
    ) -> Union[str, Any, ApiError]:
        """
        Execute single command with task and args.

        Args:
            task (str): task to issue to the remote moai server.
            df (:ob: `pandas.DataFrame`): A pandas dataframe
            args (list[str], optional): The args for the task command.

        Returns:
            Any
        """
        args = args or []

        url = f"{self.client.base_url}/moai/"

        auth_headers = self.client.get_auth_headers(with_json=True)
        auth_headers = self.client.add_org_header(headers=auth_headers)

        args = [task, *args]
        cmd_args = CommandArgs(args=args)

        res = requests.post(url, json=cmd_args.dict(), headers={**auth_headers})

        logger.debug(f"Moai command response: {res}")

        response = handlers.handle_response(res)
        return response
