import logging

from rainbow_roll import response_models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    for response_model in response_models():
        logger.info(
            "Removing redundant JSON files: %s",
            response_model.__class__.__name__,
        )
        response_model.remove_redundant_json_files()
