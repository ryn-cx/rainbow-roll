import json
import uuid

from gapi import (
    INPUT_TYPE,
    GapiCustomizations,
    apply_customizations,
    update_json_schema_and_pydantic_model,
)

from rainbow_roll.constants import FILES_PATH, RAINBOW_ROLL_PATH


def update_model(name: str, customizations: GapiCustomizations | None = None) -> None:
    """Update a specific response model based on input data."""
    schema_path = RAINBOW_ROLL_PATH / f"{name}/schema.json"
    model_path = RAINBOW_ROLL_PATH / f"{name}/models.py"
    files_path = FILES_PATH / name
    update_json_schema_and_pydantic_model(files_path, schema_path, model_path, name)
    apply_customizations(model_path, customizations)


def save_file(name: str, data: INPUT_TYPE) -> None:
    """Add a new test file for a given endpoint."""
    input_folder = FILES_PATH / name
    new_json_path = input_folder / f"{uuid.uuid4()}.json"
    new_json_path.parent.mkdir(parents=True, exist_ok=True)
    new_json_path.write_text(json.dumps(data, indent=2))
