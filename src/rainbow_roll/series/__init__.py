# The page https://www.crunchyroll.com/series/GG5H5XQ0D/dan-da-dan uses
# https://www.crunchyroll.com/content/v2/cms/series/GG5H5XQ0D?locale=en-US
import logging
from typing import Any

from rainbow_roll.protocol import RainbowRollProtocol

from .models import Series

logger = logging.getLogger(__name__)


class SeriesMixin(RainbowRollProtocol):
    def download_series(
        self,
        series_id: str,
        *,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        params = {"locale": locale}

        # This referer is valid, but it's not the ideal one because the real one would
        # include the series slug at the end as well.
        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}

        return self._get_api_request(
            endpoint="content/v2/cms/series/" + series_id,
            params=params,
            headers=headers,
        )

    def parse_series(self, data: dict[str, Any], *, update: bool = False) -> Series:
        if update:
            return self._parse_response(Series, data, "series")

        return Series.model_validate(data)

    def get_series(self, series_id: str, *, locale: str = "en-US") -> Series:
        data = self.download_series(series_id, locale=locale)
        return self.parse_series(data, update=True)
