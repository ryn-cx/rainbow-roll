import json
from pathlib import Path
from typing import Any

import pytest

from rainbow_roll import RainbowRoll
from rainbow_roll.constants import TEST_FILE_DIR


class TestParsing:
    def get_test_files(self, endpoint: str) -> list[Path]:
        """Get all JSON test files for a given endpoint."""
        dir_path = TEST_FILE_DIR / endpoint / "response"
        if not dir_path.exists():
            pytest.fail(f"No {endpoint} directory found")

        return list(dir_path.glob("*.json"))

    def test_browse_parsing(self) -> None:
        """Test that browse JSON files can be parsed without errors."""
        for json_file in self.get_test_files("browse"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client = RainbowRoll()
            client.parse_browse(data)

    def test_browse_episode_parsing(self) -> None:
        for json_file in self.get_test_files("browse_episode"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client = RainbowRoll()
            client.parse_browse(data, type="episode")

    def test_series_parsing(self) -> None:
        for json_file in self.get_test_files("series"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client = RainbowRoll()
            client.parse_series(data)

    def test_seasons_parsing(self) -> None:
        for json_file in self.get_test_files("seasons"):
            data: dict[str, Any] = json.loads(json_file.read_text())
            client = RainbowRoll()
            client.parse_seasons(data)


client = RainbowRoll()


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
