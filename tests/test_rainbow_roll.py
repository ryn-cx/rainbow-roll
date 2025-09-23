import json
from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest

from rainbow_roll import RainbowRoll
from rainbow_roll.utils.update_files import test_files_folder

client = RainbowRoll()


class TestParsing:
    def get_test_files(self, endpoint: str) -> Iterator[Path]:
        """Get all JSON test files for a given endpoint."""
        dir_path = test_files_folder(endpoint)
        if not dir_path.exists():
            pytest.fail(f"No {endpoint} directory found")

        return dir_path.glob("*.json")

    def test_browse_parsing(self) -> None:
        """Test that browse JSON files can be parsed without errors."""
        for json_file in self.get_test_files("browse"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client.parse_browse(data)

    def test_browse_episode_parsing(self) -> None:
        for json_file in self.get_test_files("browse_episode"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client.parse_browse(data, type="episode")

    def test_series_parsing(self) -> None:
        for json_file in self.get_test_files("series"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client.parse_series(data)

    def test_seasons_parsing(self) -> None:
        for json_file in self.get_test_files("seasons"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client.parse_seasons(data)


class TestGet:
    def test_get_browse_discover(self) -> None:
        client.get_browse_discover()

    def test_get_browse_videos_new(self) -> None:
        client.get_browse_videos_new()

    def test_get_series(self) -> None:
        client.get_series("GG5H5XQ0D")

    def test_get_seasons(self) -> None:
        client.get_seasons("GG5H5XQ0D")

    def test_get_episodes(self) -> None:
        client.get_episodes("G619CPMQ1")

    def test_get_browse_videos_new_date(self) -> None:
        first_page = client.get_browse_videos_new()
        last_date_on_firt_page = first_page.data[-1].last_public

        response = client.get_browse_videos_new(
            end_date=last_date_on_firt_page - timedelta(days=1),
        )
        # Make sure 2 pages of results were fetched
        assert len(response.data) == 72  # noqa: PLR2004
