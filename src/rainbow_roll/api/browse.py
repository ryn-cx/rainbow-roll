# The page https://www.crunchyroll.com/videos/new uses
# https://www.crunchyroll.com/content/v2/discover/browse?n=36&sort_by=newly_added&ratings=true&preferred_audio_language=ja-JP&locale=en-US
# The app uses https://www.crunchyroll.com/content/v2/discover/browse?n=36&sort_by=newly_added&ratings=true&locale=en-US
import logging
from datetime import datetime
from typing import Any, Literal, overload

from rainbow_roll.api.rainbow_roll_protocol import RainbowRollProtocol
from rainbow_roll.models.response.browse import ModelItem as BaseModelItem
from rainbow_roll.models.response.browse_episode import ModelItem as EpisodeModelItem

logger = logging.getLogger(__name__)


class Browse(RainbowRollProtocol):
    def download_browse(  # noqa: PLR0913
        self,
        *,
        n: int,
        sort_by: str = "newly_added",
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
        type: Literal["episode"] | None = None,  # noqa: A002
        start: int | None = None,
        ratings: Literal[True] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"sort_by": sort_by, "locale": locale, "n": n}

        if preferred_audio_language is not None:
            params["preferred_audio_language"] = preferred_audio_language

        if type is not None:
            params["type"] = type

        if start is not None:
            params["start"] = start

        if ratings is not None:
            params["ratings"] = "true"

        return self.get_api_request(
            endpoint="content/v2/discover/browse",
            params=params,
        )

    @overload
    def parse_browse(
        self,
        data: dict[str, Any],
        type: Literal["episode"],
    ) -> EpisodeModelItem: ...

    @overload
    def parse_browse(
        self,
        data: dict[str, Any],
        type: None = None,
    ) -> BaseModelItem: ...

    def parse_browse(
        self,
        data: dict[str, Any],
        type: Literal["episode"] | None = None,  # noqa: A002
    ) -> BaseModelItem | EpisodeModelItem:
        if type is None:
            return self.parse_response(BaseModelItem, data, "browse")
        if type == "episode":
            return self.parse_response(EpisodeModelItem, data, "browse_episode")

        msg = f"Unsupported type for browse: {type}"
        raise ValueError(msg)

    @overload
    def get_browse(
        self,
        *,
        n: int,
        sort_by: str = "newly_added",
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
        type: None = None,
        start: int | None = None,
        ratings: Literal[True] | None = None,
    ) -> BaseModelItem: ...

    @overload
    def get_browse(
        self,
        *,
        n: int,
        sort_by: str = "newly_added",
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
        type: Literal["episode"],
        start: int | None = None,
        ratings: Literal[True] | None = None,
    ) -> EpisodeModelItem: ...

    def get_browse(  # noqa: PLR0913
        self,
        *,
        n: int,
        sort_by: str = "newly_added",
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
        type: Literal["episode"] | None = None,  # noqa: A002
        start: int | None = None,
        ratings: Literal[True] | None = None,
    ) -> BaseModelItem | EpisodeModelItem:
        data = self.download_browse(
            n=n,
            sort_by=sort_by,
            preferred_audio_language=preferred_audio_language,
            locale=locale,
            type=type,
            start=start,
            ratings=ratings,
        )

        return self.parse_browse(data, type=type)

    def get_browse_videos_new(  # noqa: PLR0913
        self,
        *,
        n: int = 36,
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
        start: int | None = None,
        sort_by: str = "newly_added",
        ratings: Literal[True] | None = True,
        end_date: datetime | None = None,
    ) -> BaseModelItem:
        """Browse with parameters that match the internal parameters for new videos.

        When browsing https://www.crunchyroll.com/videos/new you will receive a URL like
        https://www.crunchyroll.com/content/v2/discover/browse?n=36&sort_by=newly_added&ratings=true&preferred_audio_language=ja-JP&locale=en-US
        this will exactly match that URL structure.
        """
        # For simplicity if no end_date is given set it to the current date so only 1
        # page will be downloaded.
        if end_date is None:
            end_date = datetime.now().astimezone()

        # Download current page
        data = self.download_browse(
            n=n,
            sort_by=sort_by,
            preferred_audio_language=preferred_audio_language,
            locale=locale,
            start=start,
            ratings=ratings,
        )
        result = self.parse_browse(data)

        # Recursively download pages until the last item is older than end_date or no
        # more items are available.
        if result.data and result.data[-1].last_public > end_date:
            next_pages = self.get_browse_videos_new(
                n=n,
                preferred_audio_language=preferred_audio_language,
                locale=locale,
                start=(start or 0) + n,
                sort_by=sort_by,
                ratings=ratings,
                end_date=end_date,
            )

            result.data.extend(next_pages.data)

        return result

    def get_browse_discover(
        self,
        *,
        n: int = 100,
        preferred_audio_language: str | None = None,
        locale: str = "en-US",
        start: int | None = None,
        sort_by: str = "newly_added",
    ) -> EpisodeModelItem:
        """Browse with parameters that match the internal parameters for discover.

        When browsing https://www.crunchyroll.com/discover you will receive a URL like
        https://www.crunchyroll.com/content/v2/discover/browse?type=episode&sort_by=newly_added&n=100&preferred_audio_language=ja-JP&locale=en-US
        this will exactly match that URL structure.
        """
        data = self.download_browse(
            n=n,
            sort_by=sort_by,
            preferred_audio_language=preferred_audio_language,
            locale=locale,
            start=start,
            type="episode",
        )

        return self.parse_browse(data, type="episode")
