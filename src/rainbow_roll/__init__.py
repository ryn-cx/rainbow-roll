import base64
import logging
import re
import uuid
from datetime import datetime, timedelta
from typing import Any, overload

import requests
from pydantic import BaseModel, ValidationError

from rainbow_roll.browse_series import BrowseSeriesMixin
from rainbow_roll.browse_series.models import BrowseSeries
from rainbow_roll.episodes import EpisodesMixin
from rainbow_roll.episodes.models import Episodes
from rainbow_roll.exceptions import HTTPError
from rainbow_roll.seasons import SeasonsMixin
from rainbow_roll.seasons.models import Seasons
from rainbow_roll.series import SeriesMixin
from rainbow_roll.series.models import Series
from rainbow_roll.update_files import Updater

RESPONSE_MODELS = BrowseSeries | Series | Seasons | Episodes
DEVICE_ID = uuid.uuid4().hex

logger = logging.getLogger(__name__)


class RainbowRoll(BrowseSeriesMixin, SeriesMixin, SeasonsMixin, EpisodesMixin):
    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        # These values were chosen to match the CrunchyRoll app on Windows.
        device_id: str = DEVICE_ID,
        device_type: str = "Microsoft Edge on Windows",
    ) -> None:
        self.anonymous = not (username and password)
        self.username = username
        self.password = password
        self.expiration = datetime.now().astimezone()
        self.device_id = device_id
        self.device_type = device_type
        self.public_token = ""
        self.access_token = ""
        self.refresh_token = ""
        self.domain = "beta-api.crunchyroll.com"

    def _get_public_token(self) -> str:
        """Get a public token from Crunchyroll."""
        if not self.public_token:
            url = "https://static.crunchyroll.com/vilos-v2/web/vilos/js/bundle.js"
            logger.info("Downloading public token from %s", url)
            response = requests.get(url, timeout=30)
            response_text = response.text

            if not (match := re.search(r'prod="([\w-]+:[\w-]+)"', response_text)):
                msg = "Failed to extract token from bundle.js"
                raise ValueError(msg)

            encoded_public_token = match.group(1)
            self.public_token = base64.b64encode(
                encoded_public_token.encode("iso-8859-1"),
            ).decode()

        return self.public_token

    def _get_access_token(self) -> str:
        if self.access_token and self.expiration > datetime.now().astimezone():
            return self.access_token

        if self.anonymous:
            response = requests.post(
                f"https://{self.domain}/auth/v1/token",
                headers={"Authorization": f"Basic {self._get_public_token()}"},
                data={
                    "grant_type": "client_id",
                    "device_id": self.device_id,
                    "device_type": self.device_type,
                },
                timeout=10,
            )
            parsed_response = response.json()
        else:
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

            response = requests.post(
                f"https://{self.domain}/auth/v1/token",
                headers={"Authorization": f"Basic {self._get_public_token()}"},
                data=data,
                timeout=10,
            )
            parsed_response = response.json()
            self.refresh_token = parsed_response["refresh_token"]

        self.access_token = parsed_response["access_token"]
        self.expiration = datetime.now().astimezone() + timedelta(
            seconds=parsed_response["expires_in"],
        )
        return self.access_token

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
        logger.info("Downloading API data from %s", url)
        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            timeout=60,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f"Unexpected response status code: {response.status_code}"
            raise HTTPError(msg)

        return response.json()

    def _parse_response[T: BaseModel](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
    ) -> T:
        try:
            return response_model.model_validate(data)
        except ValidationError as e:
            updater = Updater(name)
            updater.add_test_file(data)
            updater.generate_schema()
            updater.remove_redundant_files()
            msg = "Parsing error, Pydantic updated, try again."
            raise ValueError(msg) from e

    @overload
    def dump_response(self, data: list[RESPONSE_MODELS]) -> list[dict[str, Any]]: ...
    @overload
    def dump_response(self, data: RESPONSE_MODELS) -> dict[str, Any]: ...
    def dump_response(
        self,
        data: RESPONSE_MODELS | list[RESPONSE_MODELS],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Dump an API response to a JSON serializable object."""
        if isinstance(data, list):
            return [self.dump_response(response) for response in data]

        return data.model_dump(mode="json", by_alias=True, exclude_unset=True)
