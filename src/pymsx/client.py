"""MsxClient class for connecting to remote instance.

Classes
    MsxClient

Functions
    handle_unknown_response(msg: Optional[str] = None) -> ApiError
"""
import logging
from typing import Optional

import requests
from dacite import from_dict
from requests import Response

from pymsx.api.datasets import Datasets
from pymsx.config import Configuration, app_config
from pymsx.exceptions import ApiResponseError, InvalidTokenError
from pymsx.schemas import ApiError, ApiMessage, Credentials, HealthStatus, TokenResponse

logger = logging.getLogger(__name__)


class MsxClient:
    """
    Main class for access to remote msx functionality.

    Note:
        An email, password, or token is required to connect. If passed in, they will
        be used. If not, environment variables will be checked. If all these fails,
        the construction of this class will fail.

    Args:
        email (str, optional): email used to connect
        password (str, optional): password used to connect
        token (str, optional): the token used to connect

    Attributes:
        validated (bool): whether the token stored is valid
        base_url (str): the url the client is connecting to
        org_id (str): id of the organization currently connected
        email (str, optional): email if provided
        password (str, optional): password if provided
        token (str): the token being used to communicate to the remote msx server
    """

    validated: bool = False
    base_url: str
    org_id: str

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ):
        """Create a connection to org's remote msx instance."""
        config = self.config

        self.base_url = config.base_url
        self.token = token or config.token
        self.email = email or config.email
        self.password = password or config.password

        if self.token is None and self.email is None and self.password is None:
            raise ValueError("Either a token or email/password is required.")

        try:
            _ = self.connect()
            logger.info(f"Sucessfully connected to msx server {self.org_id}")
            self.validated = True
        except ApiResponseError as e:
            logger.error(f"Error connecting: {e.error}")
            if "You are not authorized to make this request" in e.error:
                raise InvalidTokenError
            else:
                raise e

        self.datasets = Datasets(self)

    @property
    def config(self) -> Configuration:
        """Get runtime application config."""
        return app_config()

    # Internal helpers

    def __get_creds(self) -> Credentials:
        creds = {"email": self.email, "password": self.password}
        return from_dict(data=creds, data_class=Credentials)

    # TODO: Check for exceptions
    def get_token(self) -> TokenResponse:
        """Request new token from api server."""
        if self.email is None or self.password is None:
            raise AttributeError("email and password required to retrieve token.")

        url = f"{self.base_url}/token"
        headers = self.get_auth_headers(with_json=True, with_token=False)
        creds = self.__get_creds()

        logger.debug(
            f"Requesting token using url={url}, " "headers={headers}, creds={creds}"
        )

        res = requests.post(url, json=creds.dict(), headers=headers)
        response = handle_auth_response(res)

        logger.debug("Recieved token response: ", response)

        if isinstance(response, dict):
            token_response: TokenResponse = from_dict(
                data=res.json(), data_class=TokenResponse
            )

            self.token = token_response.token
            self.org_id = token_response.orgId

            return token_response
        elif isinstance(response, ApiError):
            raise ApiResponseError(error=response)
        else:
            raise ApiResponseError()

    def get_auth_headers(
        self, with_json: bool = False, with_token: bool = True
    ) -> dict[str, str]:
        """Get auth headers."""
        headers: dict[str, str] = {}
        if with_token:
            headers = {**headers, "Authorization": f"Bearer {self.token}"}

        if with_json:
            headers = {**headers, "Content-Type": "application/json"}

        return headers

    # Authentication & validation

    def add_org_header(self, headers: Optional[dict[str, str]]) -> dict[str, str]:
        """Add custom org header to requests."""
        org_header = self.config.org_header
        return {**(headers or {}), org_header: self.org_id}

    def validate_token(self) -> ApiMessage:
        """Validate token with remote server."""
        headers = self.get_auth_headers(with_json=False)
        url = f"{self.base_url}/validate"
        req = requests.get(url, headers=headers)
        res = req.json()

        if "message" in res:
            # success message
            return from_dict(data=res, data_class=ApiMessage)
        elif "error" in res:
            # error message
            error = res["error"]
            logger.error(f"Error validating: {error}")
            if "You are not authorized to make this request" in res["error"]:
                raise InvalidTokenError
            else:
                raise ApiResponseError(error=from_dict(data=res, data_class=ApiError))
        else:
            # unknown
            raise ApiResponseError(error=handle_unknown_response())

    def connect(self) -> ApiMessage:
        """Connect to msx using supplied credentials."""
        if self.token is None or self.token == "":
            # try and retrieve an api token
            logger.debug("Fetching token in connect.")
            self.get_token()

        validated = self.validate_token()

        return validated

    # Api calls

    def health(self) -> HealthStatus:
        """Query the current health of the server."""
        url = f"{self.base_url}/health"
        headers = self.get_auth_headers()
        headers = self.add_org_header(headers=headers)

        logger.debug(f"Api request using headers={headers}")

        req = requests.get(url, headers=headers)
        res = req.json()

        if "error" in res:
            raise ApiResponseError(error=from_dict(data=res, data_class=ApiError))
        else:
            return from_dict(data=res, data_class=HealthStatus)


def handle_auth_response(res: Response):
    """Handle authentication responses."""
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
