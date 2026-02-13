"""Series API endpoint."""

from __future__ import annotations

from functools import cached_property
from typing import Any, override

from rainbow_roll.base_api_endpoint import BaseEndpoint
from rainbow_roll.series import models


class Series(BaseEndpoint[models.Series]):
    """Provides methods to download, parse, and retrieve series data."""

    @cached_property
    @override
    def _response_model(self) -> type[models.Series]:
        return models.Series

    def download(
        self,
        series_id: str,
        *,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        """Downloads series data for a given series ID.

        Args:
            series_id: The ID of the series to download.
            locale: The locale for the request.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        params = {"locale": locale}

        # This referer is valid, but it's not the ideal one because the real one would
        # include the series slug at the end as well.
        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}

        return self._client.download(
            endpoint="content/v2/cms/series/" + series_id,
            params=params,
            headers=headers,
        )

    def get(self, series_id: str, *, locale: str = "en-US") -> models.Series:
        """Downloads and parses series data for a given series ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            series_id: The ID of the series to get.
            locale: The locale for the request.

        Returns:
            A Series model containing the parsed data.
        """
        data = self.download(series_id, locale=locale)
        return self.parse(data)
