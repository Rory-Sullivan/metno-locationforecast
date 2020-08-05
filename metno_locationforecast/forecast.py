"""Where the magic happens.

Classes:
    Forecast: Stores forecast data, has methods for updating, saving and loading
        data.
"""

import datetime as dt
import json
from pathlib import Path
from typing import Optional

import requests

from .config import Config
from .data_containers import Interval, Place, Variable, Data

YR_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
HTTP_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

CONFIG = Config()


class Forecast:
    """Retrieves, stores and updates forecast data.

    Attributes:
        place (Place): Location for the forecast.
        forecast_type: The type of forecast.
        user_agent: the user agent to be sent with requests.
        save_location (Path): Location to cache data.
        base_url: Base url to make requests to.
        response (requests.Response): Response object.
        json_string (str): Json data as a string.
        json: Json data as an object.
        data (dict): Weather data.

    Methods:
        save: Save data to save location.
        load: Load data from saved file.
        update: Update forecast data.
    """

    forecast_types = {"compact", "complete"}

    def __init__(
        self,
        place: Place,
        user_agent: Optional[str] = None,
        forecast_type: Optional[str] = None,
        save_location: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """Create a Forecast object.

        Args:
            place: Place object for the forecast
            user_agent: The user-agent identifier to be sent with the request
            forecast_type: The type of foreast to retrieve
            save_location: Optional; Location to cache data
            base_url: Optional; URL to make requests to
        """
        if not isinstance(place, Place):
            msg = f"{place} is not a metno_locationforecast.Place object."
            raise TypeError(msg)
        self.place = place

        if user_agent is None:
            if CONFIG.user_agent is None:
                msg = (
                    "User agent has not been provided. This must be passed as an argument or set "
                    "as a configuration."
                )
                raise ValueError(msg)
            self.user_agent = CONFIG.user_agent
        else:
            self.user_agent = user_agent

        if forecast_type is None:
            self.forecast_type = CONFIG.forecast_type
        else:
            self.forecast_type = forecast_type

        if save_location is None:
            self.save_location = Path(CONFIG.save_location)
        else:
            self.save_location = Path(save_location)

        if base_url is None:
            self.base_url = CONFIG.base_url
        else:
            self.base_url = base_url

        if (
            self.base_url == "https://api.met.no/weatherapi/locationforecast/2.0/"
            and self.forecast_type not in Forecast.forecast_types
        ):
            msg = (
                f"{self.forecast_type} is not an available forecast type. Available types are: "
                f"{Forecast.forecast_types}."
            )
            raise ValueError(msg)

        # Typing information for mypy.
        self.response: requests.Response
        self.json_string: str
        self.json: dict
        self.data: Data

    def __repr__(self):
        return (
            f"Forecast({self.place}, {self.user_agent}, {self.forecast_type}, "
            f"{self.save_location}, {self.base_url})"
        )

    def __str__(self):
        if not hasattr(self, "data"):
            return "No forecast data yet."

        forecast_string = f"Forecast for {self.place.name}:"

        for interval in self.data.intervals:
            lines = str(interval).split("\n")
            forecast_string += f"\n\t{lines[0]}"
            for line in lines[1:]:
                forecast_string += f"\n\t{line}"

        return forecast_string

    @property
    def url(self):
        """The url for requests."""
        return f"{self.base_url}{self.forecast_type}"

    @property
    def url_parameters(self):
        """Parameters to be sent with request."""
        parameters = {
            "lat": self.place.coordinates["latitude"],
            "lon": self.place.coordinates["longitude"],
        }

        if self.place.coordinates["altitude"] is not None:
            parameters["altitude"] = self.place.coordinates["altitude"]

        return parameters

    @property
    def url_headers(self):
        """Headers to be sent with request."""
        headers = {
            "User-Agent": self.user_agent,
        }
        if hasattr(self, "data"):
            headers["If-Modified-Since"] = (
                self.data.last_modified.strftime(HTTP_DATETIME_FORMAT) + "GMT"
            )

        return headers

    @property
    def file_name(self):
        """File name for caching data."""
        return (
            f"lat{self.place.coordinates['latitude']}lon{self.place.coordinates['longitude']}"
            + f"altitude{self.place.coordinates['altitude']}_{self.forecast_type}.json"
        )

    def _json_from_response(self):
        """Create json data from response.

        Side Effects:
            self.json_string
            self.json
        """
        if self.response.status_code == 304:
            self.json["status_code"] = self.response.status_code
            self.json["headers"] = dict(self.response.headers)

            self.json_string = json.dumps(self.json)

        else:
            json_string = "{"
            json_string += f'"status_code":{self.response.status_code},'
            json_string += f'"headers":{json.dumps(dict(self.response.headers))},'
            json_string += f'"data":{self.response.text}'
            json_string += "}"

            self.json_string = json_string
            self.json = json.loads(json_string)

    def _parse_json(self):
        """Retrieve weather data from json data.

        Side Effects:
            self.data
        """
        json = self.json

        last_modified = dt.datetime.strptime(json["headers"]["Last-Modified"], HTTP_DATETIME_FORMAT)
        expires = dt.datetime.strptime(json["headers"]["Expires"], HTTP_DATETIME_FORMAT)

        updated_at = dt.datetime.strptime(
            json["data"]["properties"]["meta"]["updated_at"], YR_DATETIME_FORMAT
        )

        units = json["data"]["properties"]["meta"]["units"]

        intervals = []
        for timeseries in json["data"]["properties"]["timeseries"]:
            start_time = dt.datetime.strptime(timeseries["time"], YR_DATETIME_FORMAT)

            variables = {}
            for var_name, var_value in timeseries["data"]["instant"]["details"].items():
                variables[var_name] = Variable(var_name, var_value, units[var_name])

            # Take the shortest time interval available.
            hours = 0
            if "next_1_hours" in timeseries["data"]:
                hours = 1
            elif "next_6_hours" in timeseries["data"]:
                hours = 6
            elif "next_12_hours" in timeseries["data"]:
                hours = 12

            end_time = start_time + dt.timedelta(hours=hours)

            if hours != 0:
                symbol_code = timeseries["data"][f"next_{hours}_hours"]["summary"]["symbol_code"]

                for var_name, var_value in timeseries["data"][f"next_{hours}_hours"][
                    "details"
                ].items():
                    variables[var_name] = Variable(var_name, var_value, units[var_name])
            else:
                symbol_code = None

            intervals.append(Interval(start_time, end_time, symbol_code, variables))

        self.data = Data(last_modified, expires, updated_at, units, intervals)

    def _data_outdated(self):
        return self.data.expires < dt.datetime.utcnow()

    def save(self):
        """Save data to save location."""
        if not self.save_location.exists():
            self.save_location.mkdir(parents=True)
        elif not self.save_location.is_dir():
            raise NotADirectoryError(f"Expected {self.save_location} to be a directory.")

        file_path = Path(self.save_location).joinpath(self.file_name)
        file_path.write_text(self.json_string)

    def load(self):
        """Load data from saved file."""
        file_path = Path(self.save_location).joinpath(self.file_name)
        self.json_string = file_path.read_text()
        self.json = json.loads(self.json_string)
        self._parse_json()

    def update(self) -> str:
        """Update forecast data.

        Will make a request to the MET API for data and will save the data to
        the 'save_location'. If data already exists for the forecast this will
        only request new data if the data has expired and will make the request
        using the appropriate 'If-Modified-Since' header.

        Returns:
            "Data-Not-Expired": If the data has not expired yet.
            "Data-Not-Modified": If data has expired but has not been modified
                yet.
            "Data-Modified": If new data has been acquired.
        """
        return_status = ""

        if not hasattr(self, "data"):
            file_path = Path(self.save_location).joinpath(self.file_name)
            if file_path.exists():
                self.load()

        if hasattr(self, "data") and not self._data_outdated():
            return_status = "Data-Not-Expired"
            return return_status

        self.response = requests.get(self.url, params=self.url_parameters, headers=self.url_headers)

        if self.response.status_code == 304:
            return_status = "Data-Not-Modified"
        else:
            self.response.raise_for_status()
            return_status = "Data-Modified"

        self._json_from_response()
        self.save()
        self._parse_json()

        return return_status
