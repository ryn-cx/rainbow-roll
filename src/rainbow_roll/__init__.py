import base64
import logging
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests
from gapi import AbstractGapiClient

from rainbow_roll.browse_series import BrowseSeriesMixin
from rainbow_roll.constants import RAINBOW_ROLL_PATH
from rainbow_roll.episodes import EpisodesMixin
from rainbow_roll.exceptions import HTTPError
from rainbow_roll.seasons import SeasonsMixin
from rainbow_roll.series import SeriesMixin

DEVICE_ID = uuid.uuid4().hex
DEFAULT_TIMEOUT = 30
default_logger = logging.getLogger(__name__)


class RainbowRoll(
    AbstractGapiClient,
    BrowseSeriesMixin,
    SeriesMixin,
    SeasonsMixin,
    EpisodesMixin,
):
    def client_path(self) -> Path:
        return RAINBOW_ROLL_PATH

    # PLR0913 - Need more arguements to do everything required.
    def __init__(  # noqa: PLR0913
        self,
        username: str | None = None,
        password: str | None = None,
        # These values were chosen to match the CrunchyRoll app on Windows.
        device_id: str = DEVICE_ID,
        device_type: str = "Microsoft Edge on Windows",
        logger: logging.Logger = default_logger,
        timeout: int = 30,
    ) -> None:
        self.logger = logger or default_logger
        self.timeout = timeout
        self.anonymous = not (username and password)
        self.username = username
        self.password = password
        self.expires_in = datetime.now().astimezone()
        self.device_id = device_id
        self.device_type = device_type
        self.public_token = ""
        self.access_token = ""
        self.refresh_token = ""
        self.domain = "beta-api.crunchyroll.com"
        super().__init__()

    def _get_public_token(self) -> str:
        if not self.public_token:
            self._download_public_token()

        return self.public_token

    def _download_public_token(self) -> None:
        """Get a public token from Crunchyroll."""
        url = "https://static.crunchyroll.com/vilos-v2/web/vilos/js/bundle.js"
        self.logger.info("Downloading public token: %s", url)
        response = requests.get(url, timeout=self.timeout)
        response_text = response.text

        if not (match := re.search(r'prod="([\w-]+:[\w-]+)"', response_text)):
            msg = "Failed to extract token from bundle.js"
            raise ValueError(msg)

        encoded_public_token = match.group(1)
        self.public_token = base64.b64encode(
            encoded_public_token.encode("iso-8859-1"),
        ).decode()

    def _get_access_token(self) -> str:
        if not self.access_token or self.expires_in < datetime.now().astimezone():
            self._download_access_token()

        return self.access_token

    def _download_access_token(self) -> None:
        url = f"https://{self.domain}/auth/v1/token"
        if self.anonymous:
            self.logger.info("Downloading anonymous access token: %s", url)
            data = {
                "grant_type": "client_id",
                "device_id": self.device_id,
                "device_type": self.device_type,
            }
            headers = {"Authorization": f"Basic {self._get_public_token()}"}
            response = requests.post(url, data, headers=headers, timeout=self.timeout)
            parsed_response = response.json()
        else:
            self.logger.info("Downloading logged in access token: %s", url)

            data: dict[str, Any] = {
                "scope": "offline_access",
                "device_id": self.device_id,
                "device_type": self.device_type,
            }

            if self.refresh_token:
                data["refresh_token"] = self.refresh_token
                data["grant_type"] = "refresh_token"
            else:
                data["username"] = self.username
                data["device_name"] = self.password
                data["grant_type"] = "password"

            headers = {"Authorization": f"Basic {self._get_public_token()}"}
            response = requests.post(url, data, headers=headers, timeout=self.timeout)
            parsed_response = response.json()
            self.refresh_token = parsed_response["refresh_token"]

        self.access_token = parsed_response["access_token"]
        self.expires_in = datetime.now().astimezone() + timedelta(
            seconds=parsed_response["expires_in"],
        )

    def _get_api_request(
        self,
        endpoint: str,
        params: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if headers is None:
            headers = {}
        headers["authorization"] = f"Bearer {self._get_access_token()}"

        url = f"https://{self.domain}/{endpoint}"
        self.logger.info("Downloading API data: %s", url)
        response = requests.get(url, params, headers=headers, timeout=self.timeout)

        if response.status_code != 200:  # noqa: PLR2004
            msg = f"Unexpected response status code: {response.status_code}"
            raise HTTPError(msg)

        return response.json()
