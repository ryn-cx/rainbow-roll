from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from rainbow_roll.__init__ import RESPONSE_MODELS


class RainbowRollProtocol(Protocol):
    def _get_api_request(
        self,
        endpoint: str,
        params: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]: ...

    def parse_response[T: RESPONSE_MODELS](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
    ) -> T: ...
