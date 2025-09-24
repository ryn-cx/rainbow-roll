import logging
from pathlib import Path

from gapix import GAPIX

from rainbow_roll.constants import RAINBOW_ROLL_DIR, TEST_FILE_DIR

logger = logging.getLogger(__name__)


class Updater(GAPIX):
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def output_file(self) -> Path:
        return RAINBOW_ROLL_DIR / f"models/{self.endpoint}.py"

    def input_folder(self) -> Path:
        return TEST_FILE_DIR / self.endpoint


def update_all_schemas() -> None:
    """Update all response schemas based on input data."""
    for endpoint in (TEST_FILE_DIR).glob("*"):
        if endpoint.is_dir():
            logger.info("Updating schema for %s", endpoint.name)
            updater = Updater(endpoint.name)
            updater.generate_schema()
            updater.remove_redundant_files()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    update_all_schemas()
