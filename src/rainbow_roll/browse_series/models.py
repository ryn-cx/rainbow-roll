# ruff: noqa: D100, D101
from __future__ import annotations

from typing import Any

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class ExtendedMaturityRating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    level: str | None = None
    rating: str | None = None
    system: str | None = None


class LanguagePresentation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audio_notation: str
    text_notation: str


class Award(BaseModel):
    model_config = ConfigDict(extra="forbid")
    icon_url: str
    is_current_award: bool
    is_winner: bool
    text: str


class PosterTallItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    height: int
    source: str
    type: str
    width: int


class PosterWideItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    height: int
    source: str
    type: str
    width: int


class Images(BaseModel):
    model_config = ConfigDict(extra="forbid")
    poster_tall: list[list[PosterTallItem]]
    poster_wide: list[list[PosterWideItem]]


class Livestream(BaseModel):
    model_config = ConfigDict(extra="forbid")
    countdown_visibility: int
    end_date: AwareDatetime
    episode_end_date: AwareDatetime
    episode_id: str
    episode_start_date: AwareDatetime
    images: Images
    start_date: AwareDatetime


class SeriesMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audio_locales: list[str]
    availability_notes: str
    content_descriptors: list[str] | None = None
    episode_count: int
    extended_description: str
    extended_maturity_rating: ExtendedMaturityRating
    is_dubbed: bool
    is_mature: bool
    is_simulcast: bool
    is_subbed: bool
    language_presentation: LanguagePresentation
    mature_blocked: bool
    maturity_ratings: list[str]
    season_count: int
    series_launch_year: int
    subtitle_locales: list[str]
    tenant_categories: list[str] | None = None
    awards: list[Award] | None = None
    livestream: Livestream | None = None


class Field5s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    percentage: int
    unit: str


class Field1s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    percentage: int
    unit: str


class Field2s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    percentage: int
    unit: str


class Field3s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    percentage: int
    unit: str


class Field4s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    percentage: int
    unit: str


class Rating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field_5s: Field5s = Field(..., alias="5s")
    average: str
    total: int
    field_1s: Field1s = Field(..., alias="1s")
    field_2s: Field2s = Field(..., alias="2s")
    field_3s: Field3s = Field(..., alias="3s")
    field_4s: Field4s = Field(..., alias="4s")


class Images1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    poster_tall: list[list[PosterTallItem]]
    poster_wide: list[list[PosterWideItem]]


class Datum(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    promo_description: str
    series_metadata: SeriesMetadata
    last_public: AwareDatetime
    promo_title: str
    rating: Rating
    slug_title: str
    type: str
    description: str
    images: Images1
    id: str
    slug: str
    channel_id: str
    linked_resource_key: str
    external_id: str
    new: bool


class Params(BaseModel):
    model_config = ConfigDict(extra="forbid")
    n: int
    sort_by: str
    ratings: str
    locale: str
    start: int | None = None


class Headers(BaseModel):
    model_config = ConfigDict(extra="forbid")
    referer: str


class RainbowRoll(BaseModel):
    model_config = ConfigDict(extra="forbid")
    params: Params
    headers: Headers
    url: str


class BrowseSeries(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    data: list[Datum]
    meta: dict[str, Any]
    rainbow_roll: RainbowRoll
