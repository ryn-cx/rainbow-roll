# Rainbow Roll

[![Python](https://img.shields.io/badge/python->=3.13-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

An unofficial Python API client for Crunchyroll that provides easy access to series, seasons, episodes, and browse functionality.

## Features

- **Anonymous or Authenticated**: Support for both anonymous and authenticated access
- **Type Safety**: Full Pydantic models for every endpoint.
- **Dynamically Updating Models**: Models are dynamically updated based on the response
  from the API.

## Installation

### Requirements

- Python 3.13 or higher

### Install from source

```bash
uv add git+https://github.com/ryn-cx/rainbow-roll
```

## Quick Start

### Create Client

```python
from rainbow_roll import RainbowRoll

# Create anonymous client
anonymous_client = RainbowRoll()

# Create authenticated client
authenticated_client = RainbowRoll(username="Username", password="Password")
```

### Access API

```python
# Get new releases
new_videos = client.get_browse()

# Get series information
series = client.get_series("SERIES_ID")

# Get seasons for a series
seasons = client.get_seasons("SERIES_ID")

# Get episodes for a season
episodes = client.get_episodes("SEASON_ID")
```
