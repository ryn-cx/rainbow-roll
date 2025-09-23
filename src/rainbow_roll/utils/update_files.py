import json
import logging
import uuid
from pathlib import Path
from typing import Any

import gapi

from rainbow_roll.constants import RAINBOW_ROLL_DIR, TEST_FILE_DIR

logger = logging.getLogger(__name__)


def remove_redundant_files(endpoint: Path) -> None:
    temp_output_schema = RAINBOW_ROLL_DIR / f"{endpoint.name}.model.temp.py"
    good_schema_path = output_file(endpoint.name)
    good_schema_text = good_schema_path.read_text()

    # Loop through all of the files while ignoring a specific file each time to make
    # sure each file is necessary to generate the schema.
    input_files = list(endpoint.glob("*.json"))
    for i, _ in enumerate(input_files):
        test_files = input_files[:i] + input_files[i + 1 :]
        gapi.generate_from_files(test_files, temp_output_schema)
        test_schema_text = temp_output_schema.read_text()

        if test_schema_text == good_schema_text:
            logger.info("File %s is redundant", input_files[i].name)
            input_files[i].unlink()
            remove_redundant_files(endpoint)
            return

    temp_output_schema.unlink()


def test_files_folder(endpoint: str) -> Path:
    """Get the test files folder path for a given endpoint."""
    return TEST_FILE_DIR / endpoint


def output_file(endpoint: str) -> Path:
    """Get the output file path for a given endpoint."""
    return RAINBOW_ROLL_DIR / f"models/{endpoint}.py"


def add_test_file(endpoint: str, data: dict[str, Any]) -> None:
    """Add a new test file for a given endpoint."""
    endpoint_folder = test_files_folder(endpoint)
    new_json_path = endpoint_folder / f"{uuid.uuid4()}.json"
    new_json_path.parent.mkdir(parents=True, exist_ok=True)
    new_json_path.write_text(json.dumps(data, indent=2))


def generate_schema(endpoint: str) -> None:
    """Generate a Pydantic schema from test files for a given endpoint."""
    gapi.generate_from_folder(test_files_folder(endpoint), output_file(endpoint))


def update_all_schemas() -> None:
    """Update all response schemas based on input data."""
    for endpoint in (TEST_FILE_DIR).glob("*"):
        if endpoint.is_dir():
            logger.info("Updating schema for %s", endpoint.name)
            generate_schema(endpoint.name)
            remove_redundant_files(endpoint)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    update_all_schemas()
