from typing import Any, Protocol

from pydantic import BaseModel


class RainbowRollProtocol(Protocol):
    def get_api_request(
        self,
        endpoint: str,
        params: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]: ...

    def parse_response[T: BaseModel](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
    ) -> T: ...
