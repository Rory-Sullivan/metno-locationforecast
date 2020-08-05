"""Handles retrieving configuration from a user config file.

Currently supported files are 'setup.cfg' and '.metno_locationforecast' in the
root directory. '.metno_locationforecast' takes precedence over 'setup.cfg'.

Classes:
    Config: Retrieves and stores user configuration
"""

import warnings
from configparser import ConfigParser
from pathlib import Path
from typing import Iterator, Optional


class Config:
    """Retrieves and stores user configuration.

    Attributes:
        forecast_type (str): The forecast type to use
        user_agent (Optional[str]): A user agent string
        save_location (str): Location to save data to
        base_url (str): Url for requests
        user_config_file (Optional[str]): The user config file from which the
            configuration was taken, None if no file is found
    """

    section_header = "metno-locationforecast"  # Expected section header in config file
    files = ["metno-locationforecast.ini", "setup.cfg"]  # Supported files
    cwd = Path.cwd()

    def __init__(self) -> None:
        """Create Config object with the current user configuration.

        Uses default config if no configuration is supplied.
        """
        # Default configuration
        self.user_agent: Optional[str] = None
        self.forecast_type = "compact"
        self.save_location = "./data"
        self.base_url = "https://api.met.no/weatherapi/locationforecast/2.0/"
        self.user_config_file: Optional[str] = None

        self.get_config()

    @property
    def possible_user_config_files(self) -> Iterator[Path]:
        """Generator of files to look for user configuration."""
        for file in self.files:
            if self.cwd.joinpath(file).is_file():
                yield self.cwd.joinpath(file)

    def get_user_config(self) -> dict:
        """Extract user configuration from a file.

        Returns and empty dictionary if no configuration is found.
        """
        user_config = {}

        for file in self.possible_user_config_files:

            config_parser = ConfigParser()
            config_parser.read(file.resolve())

            if self.section_header in config_parser:
                user_config = dict(config_parser[self.section_header])
                self.user_config_file = str(file.resolve())
                break

        return user_config

    def get_config(self) -> None:
        """Extract user config from file if supplied and store it in self object.

        Note this modifies the objects attributes. Attributes are changed only
        if they are supplied in a config file.
        """
        user_config = self.get_user_config()

        for key, value in user_config.items():
            if hasattr(self, key):
                setattr(self, key, value)

            else:
                msg = f"{key} is not a recognised configuration."
                warnings.warn(msg)
