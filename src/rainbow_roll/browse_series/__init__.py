# The page https://www.crunchyroll.com/videos/new uses
# https://www.crunchyroll.com/content/v2/discover/browse?n=36&sort_by=newly_added&ratings=true&locale=en-US
# https://www.crunchyroll.com/content/v2/discover/browse?start=36&n=36&sort_by=newly_added&ratings=true&locale=en-US
import logging
from datetime import datetime
from typing import Any

from rainbow_roll.browse_series import models
from rainbow_roll.protocol import RainbowRollProtocol

logger = logging.getLogger(__name__)


class BrowseSeriesMixin(RainbowRollProtocol):
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
    ) -> models.BrowseSeries:
        if update:
            return self.parse_response(models.BrowseSeries, data, "browse_series")

        return models.BrowseSeries.model_validate(data)

    def get_browse_series(
        self,
        *,
        start: int | None = None,
        n: int = 36,
        sort_by: str = "newly_added",
        ratings: str = "true",
        locale: str = "en-US",
    ) -> models.BrowseSeries:
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
    ) -> list[models.BrowseSeries]:
        """Browse all pages with parameters for new videos until end_date is reached."""
        start = 0
        n = 36
        all_data: list[models.BrowseSeries] = []

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
        input_data: models.BrowseSeries | list[models.BrowseSeries] | dict[str, Any],
    ) -> list[models.Datum]:
        """Get all of the edges for a new titles input."""
        if isinstance(input_data, list):
            result: list[models.Datum] = []
            for response in input_data:
                result.extend(self.browse_series_entries(response))
            return result

        if isinstance(input_data, dict):
            input_data = self.parse_browse_series(input_data)

        return input_data.data
