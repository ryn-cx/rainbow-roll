# The page https://www.crunchyroll.com/series/GG5H5XQ0D/dan-da-dan uses
# https://www.crunchyroll.com/content/v2/cms/seasons/G619CPMQ1/episodes?preferred_audio_language=ja-JP&locale=en-US
import logging
from typing import Any

from rainbow_roll.api.rainbow_roll_protocol import RainbowRollProtocol
from rainbow_roll.models.response.episodes import ModelItem

logger = logging.getLogger(__name__)


class Episodes(RainbowRollProtocol):
    def download_episodes(
        self,
        series_id: str,
        *,
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        params = {"locale": locale}

        if preferred_audio_language:
            params["preferred_audio_language"] = preferred_audio_language

        # TODO: This URL is not correct, the real URL would be like
        # https://www.crunchyroll.com/series/G8DHV78ZM/clevatess
        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}

        return self.get_api_request(
            endpoint=f"content/v2/cms/seasons/{series_id}/episodes",
            params=params,
            headers=headers,
        )

    def parse_episodes(self, data: dict[str, Any]) -> ModelItem:
        return self.parse_response(ModelItem, data, "episodes")

    def get_episodes(
        self,
        series_id: str,
        *,
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
    ) -> ModelItem:
        data = self.download_episodes(
            series_id,
            preferred_audio_language=preferred_audio_language,
            locale=locale,
        )

        return self.parse_episodes(data)
