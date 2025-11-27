# The page https://www.crunchyroll.com/series/GG5H5XQ0D/dan-da-dan uses
# https://www.crunchyroll.com/content/v2/cms/series/GG5H5XQ0D/seasons?force_locale=&locale=en-US
import logging
from typing import Any

from rainbow_roll.protocol import RainbowRollProtocol

from .models import Seasons

logger = logging.getLogger(__name__)


class SeasonsMixin(RainbowRollProtocol):
    def download_seasons(
        self,
        series_id: str,
        *,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        params: dict[str, str | None] = {"locale": locale, "force_locale": None}

        # This referer is valid, but it's not the ideal one because the real one would
        # include the series slug at the end as well.
        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}

        return self._get_api_request(
            endpoint=f"content/v2/cms/series/{series_id}/seasons",
            params=params,
            headers=headers,
        )

    def parse_seasons(self, data: dict[str, Any], *, update: bool = False) -> Seasons:
        if update:
            return self.parse_response(Seasons, data, "seasons")

        return Seasons.model_validate(data)

    def get_seasons(self, series_id: str, *, locale: str = "en-US") -> Seasons:
        data = self.download_seasons(series_id, locale=locale)
        return self.parse_seasons(data, update=True)
