"""Base API endpoint module."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, override

from gapi import GAPIClient
from pydantic import BaseModel

from rainbow_roll.constants import FILES_PATH

if TYPE_CHECKING:
    from pathlib import Path

    from rainbow_roll import RainbowRoll


class BaseExtractor[T: BaseModel](GAPIClient[T]):
    """Base class to extract data from API responses."""

    @cached_property
    @override
    def _root_files_path(self) -> Path:
        return FILES_PATH

    @cached_property
    def json_files_folder(self) -> Path:
        """Wrapper for tests."""
        return self._json_files_folder


class BaseEndpoint[T: BaseModel](BaseExtractor[T]):
    """Base class for API endpoints."""

    def __init__(self, client: RainbowRoll) -> None:
        """Initialize the endpoint with the RainbowRoll client."""
        self._client = client
