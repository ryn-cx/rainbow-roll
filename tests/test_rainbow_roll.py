import json
from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path

import pytest

from rainbow_roll import RainbowRoll
from rainbow_roll.constants import FILES_PATH

client = RainbowRoll()


class TestParsing:
    def get_test_files(self, endpoint: str) -> Iterator[Path]:
        """Get all JSON test files for a given endpoint."""
        dir_path = FILES_PATH / endpoint
        if not dir_path.exists():
            pytest.fail(f"{dir_path} not found")

        files = dir_path.glob("*.json")

        # Make sure at least 1 file is found
        if not any(files):
            pytest.fail(f"No test files found in {dir_path}")

        return files

    def test_browse_series_parsing(self) -> None:
        """Test that browse JSON files can be parsed without errors."""
        for json_file in self.get_test_files("browse_series"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_browse_series(file_content)
            assert file_content == client.dump_response(parsed)

    def test_series_parsing(self) -> None:
        for json_file in self.get_test_files("series"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_series(file_content)
            assert file_content == client.dump_response(parsed)

    def test_seasons_parsing(self) -> None:
        for json_file in self.get_test_files("seasons"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_seasons(file_content)
            assert file_content == client.dump_response(parsed)

    def test_episodes_parsing(self) -> None:
        for json_file in self.get_test_files("episodes"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_episodes(file_content)
            assert file_content == client.dump_response(parsed)


class TestGet:
    def test_get_browse_series(self) -> None:
        client.get_browse_series()

    def test_get_series(self) -> None:
        client.get_series("GG5H5XQ0D")

    def test_get_seasons(self) -> None:
        client.get_seasons("GG5H5XQ0D")

    def test_get_episodes(self) -> None:
        client.get_episodes("G619CPMQ1")


class TestCustomGet:
    def test_get_browse_series_since_datetime(self) -> None:
        # Get the last entry on the first page to get the date to use for the end_date
        # for get_browse_series_since_datetime
        first_page = client.get_browse_series()
        last_date_on_first_page = first_page.data[-1].last_public

        response = client.get_browse_series_since_datetime(
            end_datetime=last_date_on_first_page - timedelta(days=1),
        )

        # Each page of results has 36 entries so there should be 72 total entries.
        assert len(client.browse_series_entries(response)) == 72  # noqa: PLR2004
