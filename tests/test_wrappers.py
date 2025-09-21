from rainbow_roll import RainbowRoll


def test_get_browse_discover() -> None:
    client = RainbowRoll()
    client.get_browse_discover()


def test_get_browse_videos_new() -> None:
    client = RainbowRoll()
    client.get_browse_videos_new()


def test_get_series() -> None:
    client = RainbowRoll()
    client.get_series("GG5H5XQ0D")


def test_get_seasons() -> None:
    client = RainbowRoll()
    client.get_seasons("GG5H5XQ0D")


def test_get_episodes() -> None:
    client = RainbowRoll()
    client.get_episodes("G619CPMQ1")
