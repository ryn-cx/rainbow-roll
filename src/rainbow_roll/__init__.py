"""RainbowRoll is a client for downloading and parsing data from Crunchyroll."""

import base64
import logging
import re
import uuid
from datetime import UTC, datetime, timedelta
from logging import Logger
from typing import Any

import requests

from rainbow_roll.base_api_endpoint import BaseExtractor
from rainbow_roll.browse_series import BrowseSeries
from rainbow_roll.episodes import Episodes
from rainbow_roll.exceptions import HTTPError
from rainbow_roll.seasons import Seasons
from rainbow_roll.series import Series

DEVICE_ID = uuid.uuid4().hex
DEFAULT_TIMEOUT = 30
default_logger = logging.getLogger(__name__)


def response_models() -> list[BaseExtractor[Any]]:
    """Returns a list of all of the response models for RainbowRoll."""
    client = RainbowRoll()

    return [
        client.browse_series,
        client.series,
        client.seasons,
        client.episodes,
    ]


class RainbowRoll:
    """Interface for downloading and parsing data from Crunchyroll."""

    # PLR0913 - Need more arguements to do everything required.
    def __init__(  # noqa: PLR0913
        self,
        username: str | None = None,
        password: str | None = None,
        # These values were chosen to match the CrunchyRoll app on Windows.
        device_id: str = DEVICE_ID,
        device_type: str = "Microsoft Edge on Windows",
        logger: Logger = default_logger,
        timeout: int = 30,
    ) -> None:
        """Initialize the RainbowRoll client."""
        self.logger = logger or default_logger
        self.timeout = timeout
        self.anonymous = not (username and password)
        self.username = username
        self.password = password
        self.__token_expires_at = datetime.now(tz=UTC)
        self.device_id = device_id
        self.device_type = device_type
        self.__public_token_value = ""
        self.__access_token_value = ""
        self.__refresh_token = ""
        self.domain = "beta-api.crunchyroll.com"

        self.browse_series = BrowseSeries(self)
        self.series = Series(self)
        self.seasons = Seasons(self)
        self.episodes = Episodes(self)

        super().__init__()

    @property
    def __public_token(self) -> str:
        if not self.__public_token_value:
            self.__download_public_token()

        return self.__public_token_value

    @__public_token.setter
    def __public_token(self, value: str) -> None:
        self.__public_token_value = value

    def __download_public_token(self) -> None:
        """Get a public token from Crunchyroll."""
        url = "https://static.crunchyroll.com/vilos-v2/web/vilos/js/bundle.js"
        self.logger.info("Downloading public token: %s", url)
        response = requests.get(url, timeout=self.timeout)
        response_text = response.text

        if not (match := re.search(r'prod="([\w-]+:[\w-]+)"', response_text)):
            msg = "Failed to extract token from bundle.js"
            raise ValueError(msg)

        encoded_public_token = match.group(1)
        self.__public_token = base64.b64encode(
            encoded_public_token.encode("iso-8859-1"),
        ).decode()

    @property
    def __access_token(self) -> str:
        if not self.__access_token_value or self.__token_expires_at < datetime.now(
            tz=UTC,
        ):
            self.__download_access_token()

        return self.__access_token_value

    @__access_token.setter
    def __access_token(self, value: str) -> None:
        self.__access_token_value = value

    def __download_access_token(self) -> None:
        url = f"https://{self.domain}/auth/v1/token"
        headers = {"Authorization": f"Basic {self.__public_token}"}

        data: dict[str, Any] = {
            "device_id": self.device_id,
            "device_type": self.device_type,
        }

        if self.__refresh_token:
            self.logger.info("Refreshing access token: %s", url)
            data["grant_type"] = "refresh_token"
            data["refresh_token"] = self.__refresh_token
        elif self.anonymous:
            self.logger.info("Downloading anonymous access token: %s", url)
            data["grant_type"] = "client_id"
        else:
            self.logger.info("Downloading logged in access token: %s", url)
            data["grant_type"] = "password"
            data["scope"] = "offline_access"
            data["username"] = self.username
            data["device_name"] = self.password

        response = requests.post(url, data, headers=headers, timeout=self.timeout)
        parsed_response = response.json()

        self.__access_token = parsed_response["access_token"]
        self.__token_expires_at = datetime.now(tz=UTC) + timedelta(
            seconds=parsed_response["expires_in"],
        )

        # Refresh token are only available when the user is logged into an account.
        if "refresh_token" in parsed_response:
            self.__refresh_token = parsed_response["refresh_token"]

    def download(
        self,
        endpoint: str,
        params: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a request to the Crunchyroll API with the given endpoint."""
        if headers is None:
            headers = {}
        headers["authorization"] = f"Bearer {self.__access_token}"

        url = f"https://{self.domain}/{endpoint}"
        self.logger.info("Downloading API data: %s", url)
        response = requests.get(url, params, headers=headers, timeout=self.timeout)

        if response.status_code != 200:  # noqa: PLR2004
            msg = f"Unexpected response status code: {response.status_code}"
            raise HTTPError(msg)

        output = response.json()
        output["rainbow_roll"] = {}
        output["rainbow_roll"]["params"] = params
        headers.pop("authorization")
        output["rainbow_roll"]["headers"] = headers
        output["rainbow_roll"]["url"] = url

        return output
