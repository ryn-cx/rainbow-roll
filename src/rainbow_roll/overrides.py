from pydantic.dataclasses import dataclass

EXTRA_IMPORTS = ""


@dataclass
class Override:
    endpoint: str
    model: str
    field_name: str
    original: str
    replacement: str


override_values = []

OVERRIDES = [Override(*override_value) for override_value in override_values]
