# The page https://www.crunchyroll.com/series/GG5H5XQ0D/dan-da-dan uses
# https://www.crunchyroll.com/content/v2/cms/seasons/GR75CDJ0M/episodes?locale=en-US
from typing import Any

from rainbow_roll.episodes import models
from rainbow_roll.protocol import RainbowRollProtocol


class EpisodesMixin(RainbowRollProtocol):
    def download_episodes(
        self,
        series_id: str,
        *,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        # This referer is valid, but it's not the ideal one because the real one would
        # include the series slug at the end as well.
        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}
        endpoint = f"content/v2/cms/seasons/{series_id}/episodes"
        params = {"locale": locale}
        return self._get_api_request(endpoint=endpoint, params=params, headers=headers)

    def parse_episodes(
        self,
        data: dict[str, Any],
        *,
        update: bool = True,
    ) -> models.Episodes:
        if update:
            return self.parse_response(models.Episodes, data, "episodes")

        return models.Episodes.model_validate(data)

    def get_episodes(self, series_id: str, *, locale: str = "en-US") -> models.Episodes:
        data = self.download_episodes(series_id, locale=locale)
        return self.parse_episodes(data)
