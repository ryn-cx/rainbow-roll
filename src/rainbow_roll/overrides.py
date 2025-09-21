from pydantic import BaseModel

EXTRA_IMPORTS = """from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datetime import datetime"""


class Override(BaseModel):
    endpoint: str
    model: str
    field_name: str
    replacement: str


OVERRIDES: list[Override] = []


def override(endpoint: str, model: str, field_name: str, new_type: str) -> None:
    OVERRIDES.append(
        Override(
            endpoint=endpoint,
            model=model,
            field_name=field_name,
            replacement=f"{field_name}: {new_type}",
        ),
    )


override("browse", "Datum", "last_public", "datetime")
override("browse_episodes", "EpisodeMetadata", "episode_air_date", "datetime")
override("browse_episodes", "EpisodeMetadata", "premium_available_date", "datetime")
override("browse_episodes", "EpisodeMetadata", "upload_date", "datetime")
override("browse_episodes", "Datum", "last_public", "datetime")
