# The page https://www.crunchyroll.com/videos/new uses
# https://www.crunchyroll.com/content/v2/discover/browse?n=36&sort_by=newly_added&ratings=true&locale=en-US
# https://www.crunchyroll.com/content/v2/discover/browse?start=36&n=36&sort_by=newly_added&ratings=true&locale=en-US
import logging
from datetime import datetime
from typing import Any

from rainbow_roll.protocol import RainbowRollProtocol

from .models import Datum, Model

logger = logging.getLogger(__name__)


class BrowseSeries(RainbowRollProtocol):
    def _download_browse_series(
        self,
        *,
        start: int | None = None,
        n: int = 36,
        sort_by: str = "newly_added",
        ratings: str = "true",
        locale: str = "en-US",
    ) -> dict[str, Any]:
        # The order of the parameters marches the query even though it probably doesn't
        # matter.
        params: dict[str, Any] = {}
        # Start parameter should only be included if it has a value.
        if start is not None:
            params["start"] = start

        params["n"] = n
        params["sort_by"] = sort_by
        params["ratings"] = ratings
        params["locale"] = locale

        headers = {"referer": "https://www.crunchyroll.com/videos/new"}

        return self._get_api_request("content/v2/discover/browse", params, headers)

    def parse_browse_series(
        self,
        data: dict[str, Any],
        *,
        update: bool = False,
    ) -> Model:
        if update:
            return self._parse_response(Model, data, "browse_series")

        return Model.model_validate(data)

    def get_browse_series(
        self,
        *,
        start: int | None = None,
        n: int = 36,
        sort_by: str = "newly_added",
        ratings: str = "true",
        locale: str = "en-US",
    ) -> Model:
        data = self._download_browse_series(
            n=n,
            sort_by=sort_by,
            locale=locale,
            start=start,
            ratings=ratings,
        )

        return self.parse_browse_series(data, update=True)

    def get_browse_series_since_datetime(
        self,
        *,
        locale: str = "en-US",
        sort_by: str = "newly_added",
        ratings: str = "true",
        end_datetime: datetime | None = None,
    ) -> list[Model]:
        """Browse all pages with parameters for new videos until end_date is reached."""
        start = 0
        n = 36
        all_data: list[Model] = []

        # Stop the user from doing something silly on accident.
        if end_datetime is None:
            end_datetime = datetime.now().astimezone()

        while True:
            result = self.get_browse_series(
                n=n,
                locale=locale,
                start=start,
                sort_by=sort_by,
                ratings=ratings,
            )

            all_data.append(result)

            if result.data[-1].last_public <= end_datetime or len(result.data) < n:
                return all_data

            start += n

    def browse_series_entries(
        self,
        responses: Model | list[Model] | dict[str, Any],
    ) -> list[Datum]:
        """Get all of the edges for a new titles input."""
        if isinstance(responses, list):
            result: list[Datum] = []
            for response in responses:
                result.extend(self.browse_series_entries(response))
            return result

        if isinstance(responses, dict):
            responses = self.parse_browse_series(responses)

        return responses.data
