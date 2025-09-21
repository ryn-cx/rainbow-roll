import json
import subprocess
from pathlib import Path

import datamodel_code_generator

from rainbow_roll.constants import RAINBOW_ROLL_DIR, TEST_FILE_DIR
from rainbow_roll.overrides import EXTRA_IMPORTS, OVERRIDES, Override


def combine_json_files(input_folder: Path) -> str:
    input_files = input_folder.glob("*.json")
    input_contents = [file.read_bytes() for file in input_files]
    input_parsed = [json.loads(content) for content in input_contents]
    return json.dumps(input_parsed)


def apply_overrides(lines: list[str], name: str) -> None:
    for override in OVERRIDES:
        apply_override(lines, override, name)


def apply_override(lines: list[str], override: Override, name: str) -> None:
    """Replace specific field definitions in the generated code.

    Args:
        lines: List of code lines to modify
        override: Override configuration specifying model, field, and replacement
        name: Name of the file being processed

    Raises:
        ValueError: If the override target is not found
    """
    if name != f"{override.endpoint}.py":
        return

    current_class = None

    for i, line in enumerate(lines):
        if line.startswith("class ") and line.endswith(":"):
            current_class = line.split("class ")[1].split("(")[0]
            continue

        if current_class != override.model:
            continue

        if line.startswith(f"    {override.field_name}:"):
            lines[i] = f"    {override.replacement}"
            return

    # If we reach here, the override wasn't applied
    msg = (
        "Unable to apply override "
        f"{override.endpoint}.{override.model}.{override.field_name}"
    )
    raise ValueError(msg)


def add_extra_imports(lines: list[str], extra_imports: str) -> None:
    """Add extra import statements to the generated code.

    Args:
        lines: List of code lines to modify
        extra_imports: String containing extra import statements to add
    """
    line_with_first_class = next(
        (i for i, line in enumerate(lines) if line.startswith("class ")),
    )
    lines.insert(line_with_first_class, extra_imports)


def generate_schema(input_data: str, output_file: Path) -> None:
    """Generate a Pydantic model schema from JSON data."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    datamodel_code_generator.generate(
        input_=input_data,
        output=output_file,
        input_file_type=datamodel_code_generator.InputFileType.Json,
        output_model_type=datamodel_code_generator.DataModelType.PydanticV2BaseModel,
        snake_case_field=True,
        disable_timestamp=True,
        extra_fields="forbid",
        target_python_version=datamodel_code_generator.PythonVersion.PY_313,
    )

    lines = output_file.read_text().splitlines()
    apply_overrides(lines, output_file.name)
    add_extra_imports(lines, EXTRA_IMPORTS)

    # Remove the last 3 lines which will contain the extra wrapper class used to combine
    # files into a single json file which is not actually used by the API
    lines = "\n".join(lines[:-3])
    output_file.write_text(lines)

    subprocess.run(
        ["uv", "run", "ruff", "check", "--fix", str(output_file)],  # noqa: S607
        check=False,
    )
    subprocess.run(
        ["uv", "run", "ruff", "format", str(output_file)],  # noqa: S607
        check=False,
    )


def update_response(endpoint: Path) -> None:
    """Update the response schema for a given endpoint."""
    response_input_dumped = combine_json_files(endpoint / "response")
    output_schema = RAINBOW_ROLL_DIR / f"models/response/{endpoint.name}.py"
    generate_schema(response_input_dumped, output_schema)


def update_all_schemas() -> None:
    """Update all response schemas based on input data."""
    for endpoint in TEST_FILE_DIR.glob("*"):
        if endpoint.is_dir():
            update_response(endpoint)


if __name__ == "__main__":
    update_all_schemas()
