import json
import logging
from pathlib import Path

from rainbow_roll.constants import RAINBOW_ROLL_DIR, TEST_FILE_DIR
from rainbow_roll.utils.update_files import generate_schema, update_response

logger = logging.getLogger(__name__)


def shake_files(endpoint: Path, file_type: str) -> None:
    """Check for redundant files in either request or response directories."""
    input_files = list((endpoint / file_type).glob("*.json"))
    logger.info(
        "Checking %s %s with %d files",
        endpoint.name,
        file_type,
        len(input_files),
    )

    output_schema = RAINBOW_ROLL_DIR / f"temp/{file_type}/{endpoint.name}.py"
    good_schema_path = RAINBOW_ROLL_DIR / f"models/{file_type}/{endpoint.name}.py"
    good_schema = good_schema_path.read_text()

    # Loop through all of the files while ignoring a specific file each time to make
    # sure each file is necessary to generate the schema.
    for i, _ in enumerate(input_files):
        test_files = input_files[:i] + input_files[i + 1 :]
        input_contents = [file.read_text() for file in test_files]
        input_parsed = [json.loads(content) for content in input_contents]
        response_input_dumped = json.dumps(input_parsed)
        generate_schema(response_input_dumped, output_schema)
        test_schema = output_schema.read_text()

        if test_schema == good_schema:
            logger.warning("File %s is redundant", input_files[i].name)
            input_files[i].unlink()
            shake_files(endpoint, file_type)
            return


def shake_response(endpoint: Path) -> None:
    """Check for redundant response files."""
    update_response(endpoint)
    shake_files(endpoint, "response")


def shake_all_schemas() -> None:
    for endpoint in TEST_FILE_DIR.glob("*"):
        if endpoint.is_dir():
            shake_response(endpoint)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    shake_all_schemas()
