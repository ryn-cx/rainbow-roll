import json
from pathlib import Path

import datamodel_code_generator
from datamodel_code_generator.format import Formatter

from rainbow_roll.constants import RAINBOW_ROLL_DIR, TEST_FILE_DIR


def combine_json_files(input_folder: Path) -> str:
    input_files = input_folder.glob("*.json")
    input_contents = [file.read_bytes() for file in input_files]
    input_parsed = [json.loads(content) for content in input_contents]
    return json.dumps(input_parsed)


def generate_schema(input_data: str, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    datamodel_code_generator.generate(
        input_=input_data,
        output=output_file,
        input_file_type=datamodel_code_generator.InputFileType.Json,
        output_model_type=datamodel_code_generator.DataModelType.PydanticV2BaseModel,
        snake_case_field=True,
        disable_timestamp=True,
        extra_fields="forbid",
        formatters=[Formatter.RUFF_CHECK, Formatter.RUFF_FORMAT],
        target_python_version=datamodel_code_generator.PythonVersion.PY_313,
    )

    # Remove the last 3 lines which will contain the extra wrapper class used to combine
    # files into a single json file which is not actually used by the API
    lines = output_file.read_text().splitlines()
    lines = "\n".join(lines[:-3])

    output_file.write_text(lines)


def update_response(endpoint: Path) -> None:
    response_input_dumped = combine_json_files(endpoint / "response")
    output_schema = RAINBOW_ROLL_DIR / f"models/response/{endpoint.name}.py"
    generate_schema(response_input_dumped, output_schema)


def update_all_schemas() -> None:
    for endpoint in TEST_FILE_DIR.glob("*"):
        if endpoint.is_dir():
            update_response(endpoint)


if __name__ == "__main__":
    update_all_schemas()
