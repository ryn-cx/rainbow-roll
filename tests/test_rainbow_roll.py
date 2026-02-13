"""Tests for the rainbow_roll library."""

import json
from datetime import timedelta

from rainbow_roll import RainbowRoll

client = RainbowRoll()


class TestParsing:
    """Tests for parsing saved JSON files into Pydantic models."""

    def test_parse_browse_series(self) -> None:
        """Parse all saved browse series JSON files."""
        for json_file in client.browse_series.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.browse_series.parse(file_content)

    def test_parse_series(self) -> None:
        """Parse all saved series JSON files."""
        for json_file in client.series.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.series.parse(file_content)

    def test_parse_seasons(self) -> None:
        """Parse all saved seasons JSON files."""
        for json_file in client.seasons.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.seasons.parse(file_content)

    def test_parse_episodes(self) -> None:
        """Parse all saved episodes JSON files."""
        for json_file in client.episodes.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.episodes.parse(file_content)


class TestGet:
    """Tests for downloading and parsing live data from Crunchyroll."""

    def test_get_browse_series(self) -> None:
        """Download and parse browse series."""
        client.browse_series.get()

    def test_get_series(self) -> None:
        """Download and parse a series."""
        client.series.get("GG5H5XQ0D")

    def test_get_seasons(self) -> None:
        """Download and parse seasons."""
        client.seasons.get("GG5H5XQ0D")

    def test_get_episodes(self) -> None:
        """Download and parse episodes."""
        client.episodes.get("G619CPMQ1")


class TestCustomGet:
    """Tests for custom endpoint methods."""

    def test_get_browse_series_since_datetime(self) -> None:
        """Download and parse browse series since a datetime."""
        # Get the last entry on the first page to get the date to use for the end_date
        # for get_since_datetime
        first_page = client.browse_series.get()
        last_date_on_first_page = first_page.data[-1].last_public

        response = client.browse_series.get_since_datetime(
            end_datetime=last_date_on_first_page - timedelta(days=1),
        )

        # Each page of results has 36 entries so there should be at least 36 entries.
        assert len(client.browse_series.entries(response)) >= 36  # noqa: PLR2004
