# The page https://www.crunchyroll.com/videos/new uses
# https://www.crunchyroll.com/content/v2/discover/browse?n=36&sort_by=newly_added&ratings=true&locale=en-US
# https://www.crunchyroll.com/content/v2/discover/browse?start=36&n=36&sort_by=newly_added&ratings=true&locale=en-US
from datetime import datetime
from typing import Any

from rainbow_roll.browse_series import models
from rainbow_roll.protocol import RainbowRollProtocol


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
        params: dict[str, str | int] = {
            "n": n,
            "sort_by": sort_by,
            "ratings": ratings,
            "locale": locale,
        }

        if start is not None:
            params["start"] = start

        headers = {"referer": "https://www.crunchyroll.com/videos/new"}

        return self._get_api_request("content/v2/discover/browse", params, headers)

    def parse_browse_series(
        self,
        data: dict[str, Any],
        *,
        update: bool = True,
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

        return self.parse_browse_series(data)

    def get_browse_series_since_datetime(
        self,
        *,
        n: int = 36,
        locale: str = "en-US",
        sort_by: str = "newly_added",
        ratings: str = "true",
        end_datetime: datetime | None = None,
    ) -> list[models.BrowseSeries]:
        """Browse all pages with parameters for new videos until end_date is reached."""
        start = 0
        all_data: list[models.BrowseSeries] = []
        end_datetime = end_datetime or datetime.now().astimezone()

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
        data: models.BrowseSeries | list[models.BrowseSeries],
    ) -> list[models.Datum]:
        """Get all of the edges for a new titles input."""
        if isinstance(data, models.BrowseSeries):
            return data.data

        return [
            datum for response in data for datum in self.browse_series_entries(response)
        ]
