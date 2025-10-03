import json
import logging
import uuid
from typing import Any

from gapi import generate_from_folder

from rainbow_roll.constants import RAINBOW_ROLL_DIR, TEST_FILE_DIR

logger = logging.getLogger(__name__)


def update_all_models() -> None:
    """Update all response models based on input data."""
    for endpoint in (TEST_FILE_DIR).glob("*"):
        update_model(endpoint.name)


def update_model(name: str) -> None:
    """Update a specific response model based on input data."""
    input_folder = TEST_FILE_DIR / name
    output_folder = RAINBOW_ROLL_DIR / f"{name}/models.py"
    class_name = name.replace("_", " ").title().replace(" ", "")
    logger.info("Updating schema for %s", name)
    generate_from_folder(
        input_folder,
        output_folder,
        class_name,
        remove_redundant_files=True,
    )


def add_test_file(name: str, data: dict[str, Any]) -> None:
    """Add a new test file for a given endpoint."""
    # Assume this function will only ever be used for responses.
    input_folder = TEST_FILE_DIR / name
    new_json_path = input_folder / f"{uuid.uuid4()}.json"
    new_json_path.parent.mkdir(parents=True, exist_ok=True)
    new_json_path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    update_all_models()
