<div align="center">

# Rainbow Roll

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/ryn-cx/rainbow-roll/refs/heads/master/pyproject.toml)
![GitHub License](https://img.shields.io/github/license/ryn-cx/rainbow-roll)
![GitHub Issues](https://img.shields.io/github/issues/ryn-cx/rainbow-roll)

**An unofficial Python API client for Crunchyroll**

</div>

## Features

- **Anonymous or Authenticated** - Support for both anonymous and authenticated access
- **Type Safety** - Full Pydantic models for every endpoint with robust data validation
- **Self-Updating Models** - Models are automatically updated when the API response structure changes

## Installation

Requires Python 3.13+

```bash
uv add git+https://github.com/ryn-cx/rainbow-roll
```

## Quick Start

```python
from rainbow_roll import RainbowRoll

# Anonymous client
client = RainbowRoll()

# Authenticated client
client = RainbowRoll(username="your_username", password="your_password")
```

### Browse Series

```python
browse = client.browse_series.get()
```

### Series

```python
series = client.series.get("SERIES_ID")
```

### Seasons

```python
seasons = client.seasons.get("SERIES_ID")
```

### Episodes

```python
episodes = client.episodes.get("SEASON_ID")
```

## Two-Step API

Every endpoint supports a two-step `download()` / `parse()` workflow for cases where you want to inspect or cache the raw JSON before parsing:

```python
raw = client.browse_series.download()
parsed = client.browse_series.parse(raw)

raw = client.series.download("SERIES_ID")
parsed = client.series.parse(raw)
```
