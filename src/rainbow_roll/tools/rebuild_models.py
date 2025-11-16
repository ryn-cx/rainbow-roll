from gapi import update_json_schema_and_pydantic_model

from rainbow_roll.constants import FILES_PATH, RAINBOW_ROLL_PATH

if __name__ == "__main__":
    for input_folder in FILES_PATH.iterdir():
        if input_folder.name == ".git":
            continue
        name = input_folder.name
        schema_path = RAINBOW_ROLL_PATH / f"{name}/schema.json"
        model_path = RAINBOW_ROLL_PATH / f"{name}/models.py"

        schema_path.unlink(missing_ok=True)
        model_path.unlink(missing_ok=True)

        json_files = list(input_folder.glob("*.json"))
        update_json_schema_and_pydantic_model(json_files, schema_path, model_path, name)
