"""Handles retrieving configuration from config file.

Currently supported files are 'setup.cfg' and '.metno_locationforecast'.
'.metno_locationforecast' takes precedence over 'setup.cfg'
"""

from configparser import ConfigParser
from pathlib import Path
from typing import Iterator

SECTION_HEADER = "metno_locationforecast"
FILES = [".metno_locationforecast", "setup.cfg"]
CWD = Path.cwd()


def get_possible_user_config_files() -> Iterator[Path]:
    for file in FILES:
        if CWD.joinpath(file).is_file():
            yield CWD.joinpath(file)


def get_user_config() -> dict:
    user_config = {}

    for file in get_possible_user_config_files():

        config_parser = ConfigParser()
        config_parser.read(file.absolute())

        if SECTION_HEADER in config_parser:
            user_config = dict(config_parser[SECTION_HEADER])
            break

    return user_config


def get_config() -> dict:

    # Set default configurations.
    config = {
        "forecast_type": None,
        "user_agent": None,
        "save_location": "./data",
        "base_url": "https://api.met.no/weatherapi/locationforecast/2.0/",
    }

    user_config = get_user_config()

    for key in config.keys():
        if key in user_config:
            config[key] = user_config[key]

    return config
