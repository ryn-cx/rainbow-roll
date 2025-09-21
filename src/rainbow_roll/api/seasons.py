# The page https://www.crunchyroll.com/series/GG5H5XQ0D/dan-da-dan uses
# https://www.crunchyroll.com/content/v2/cms/series/GG5H5XQ0D/seasons?force_locale=&preferred_audio_language=ja-JP&locale=en-US
# The Windows app uses https://www.crunchyroll.com/content/v2/cms/series/G8DHV78ZM/seasons?force_locale=&locale=en-US
import logging
from typing import Any

from rainbow_roll.api.rainbow_roll_protocol import RainbowRollProtocol
from rainbow_roll.models.response.seasons import ModelItem

logger = logging.getLogger(__name__)


class Seasons(RainbowRollProtocol):
    def download_seasons(
        self,
        series_id: str,
        *,
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        params: dict[str, str | None] = {"locale": locale, "force_locale": None}

        if preferred_audio_language:
            params["preferred_audio_language"] = preferred_audio_language

        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}

        return self.get_api_request(
            endpoint=f"content/v2/cms/series/{series_id}/seasons",
            params=params,
            headers=headers,
        )

    def parse_seasons(self, data: dict[str, Any]) -> ModelItem:
        return self.parse_response(ModelItem, data, "seasons")

    def get_seasons(
        self,
        series_id: str,
        *,
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
    ) -> ModelItem:
        data = self.download_seasons(
            series_id,
            preferred_audio_language=preferred_audio_language,
            locale=locale,
        )

        return self.parse_seasons(data)
