<div align="center">

# 🌈 Rainbow Roll

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/ryn-cx/rainbow-roll/refs/heads/master/pyproject.toml)
![GitHub License](https://img.shields.io/github/license/ryn-cx/rainbow-roll)
![GitHub Issues](https://img.shields.io/github/issues/ryn-cx/rainbow-roll)

**An unofficial Python API client for Crunchyroll**

</div>

## ✨ Features

- 🔐 **Anonymous or Authenticated**: Support for both anonymous and authenticated access
- 🛡️ **Type Safety**: Full Pydantic models for every endpoint
- 🔄 **Dynamically Updating Models**: Models are dynamically updated based on the response from the API

## 📦 Installation

### Requirements

- 🐍 Python 3.13 or higher

### Install from source

```bash
uv add git+https://github.com/ryn-cx/rainbow-roll
```

## 🚀 Quick Start

### Create Client

```python
from rainbow_roll import RainbowRoll

# 🌐 Create anonymous client
anonymous_client = RainbowRoll()

# 🔐 Create authenticated client
authenticated_client = RainbowRoll(username="your_username", password="your_password")
```

### Access API

```python
# 🆕 Get new releases
new_videos = client.get_browse_series()

# 📺 Get series information
series = client.get_series("SERIES_ID")

# 📋 Get seasons for a series
seasons = client.get_seasons("SERIES_ID")

# 🎬 Get episodes for a season
episodes = client.get_episodes("SEASON_ID")
```
