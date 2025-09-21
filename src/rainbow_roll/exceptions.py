class RainbowRollError(Exception):
    """Base exception for rainbow-roll library."""


class HTTPError(RainbowRollError):
    """Raised when HTTP request fails with unexpected status code."""
