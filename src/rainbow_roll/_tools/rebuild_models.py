from rainbow_roll import RainbowRoll

if __name__ == "__main__":
    client = RainbowRoll()
    client.rebuild_models("browse_series")
    client.rebuild_models("episodes")
    client.rebuild_models("seasons")
    client.rebuild_models("series")
