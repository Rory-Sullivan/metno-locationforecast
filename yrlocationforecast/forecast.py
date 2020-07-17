"""Where the magic happens."""

import datetime as dt
import json
from pathlib import Path
from typing import Optional

import requests

from yrlocationforecast.data_containers import Interval, Place, Variable

YR_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
HTTP_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


class Forecast:
    """Class for storing a forecast.  This is a group of forecast intervals."""

    base_url = "https://api.met.no/weatherapi/locationforecast/2.0/"
    forecast_types = {"compact", "complete"}

    def __init__(
        self, place: Place, forecast_type: str, user_agent: str, save_location: str = "./data/",
    ):
        if type(place) != Place:
            msg = f"{place} is not a yrlocationforecast.Place object."
            raise TypeError(msg)
        self.place = place

        if forecast_type not in Forecast.forecast_types:
            msg = (
                f"{forecast_type} is not an available forecast type. Available types are: "
                + f"{Forecast.forecast_types}."
            )
            raise ValueError(msg)
        self.forecast_type = forecast_type

        self.user_agent = user_agent
        self.save_location = Path(save_location)

        self.response: Optional[requests.Response] = None
        self.json_string: Optional[str] = None
        self.json: Optional[dict] = None
        self.data: Optional[dict] = None

    def __repr__(self):
        return (
            f"Forecast({self.place}, {self.forecast_type}, {self.user_agent}, "
            + f"save_location={self.save_location})"
        )

    @property
    def url(self):
        return f"{self.base_url}{self.forecast_type}"

    @property
    def url_parameters(self):
        parameters = {
            "lat": self.place.coordinates["latitude"],
            "lon": self.place.coordinates["longitude"],
        }

        if self.place.coordinates["altitude"] is not None:
            parameters["altitude"] = self.place.coordinates["altitude"]

        return parameters

    @property
    def url_headers(self):
        headers = {
            "User-Agent": self.user_agent,
        }
        if self.data is not None:
            headers["If-Modified-Since"] = (
                self.data["last_modified"].strftime(HTTP_DATETIME_FORMAT) + "GMT"
            )

        return headers

    @property
    def file_name(self):
        return (
            f"lat{self.place.coordinates['latitude']}lon{self.place.coordinates['longitude']}"
            + f"altitude{self.place.coordinates['altitude']}_{self.forecast_type}.json"
        )

    def _json_from_response(self):
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
        json = self.json
        data = {}

        data["last_modified"] = dt.datetime.strptime(
            json["headers"]["Last-Modified"], HTTP_DATETIME_FORMAT
        )
        data["expires"] = dt.datetime.strptime(json["headers"]["Expires"], HTTP_DATETIME_FORMAT)

        data["updated_at"] = dt.datetime.strptime(
            json["data"]["properties"]["meta"]["updated_at"], YR_DATETIME_FORMAT
        )

        data["units"] = json["data"]["properties"]["meta"]["units"]

        data["intervals"] = []
        for timeseries in json["data"]["properties"]["timeseries"]:
            start_time = dt.datetime.strptime(timeseries["time"], YR_DATETIME_FORMAT)

            variables = []
            for var_name, var_value in timeseries["data"]["instant"]["details"].items():
                variables.append(Variable(var_name, var_value, data["units"][var_name]))

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
                    variables.append(Variable(var_name, var_value, data["units"][var_name]))

            data["intervals"].append(Interval(start_time, end_time, symbol_code, variables))

        self.data = data

    def _data_outdated(self):
        return self.data["expires"] < dt.datetime.utcnow()

    def save(self):
        """Save data to save location."""
        if not self.save_location.exists():
            self.save_location.mkdir(parents=True)
        elif not self.save_location.is_dir():
            raise NotADirectoryError(f"Expected {self.save_location} to be a directory.")

        file_path = Path(self.save_location).joinpath(self.file_name)
        file_path.write_text(self.json_string)

    def load(self):
        """Load data from save location."""
        file_path = Path(self.save_location).joinpath(self.file_name)
        self.json_string = file_path.read_text()
        self.json = json.loads(self.json_string)
        self._parse_json()

    def update(self):
        """Update forecast data."""
        if self.data is None:
            file_path = Path(self.save_location).joinpath(self.file_name)
            if file_path.exists():
                self.load()

        if self.data is not None and not self._data_outdated():
            print("Data has not expired.")
            return

        self.response = requests.get(self.url, params=self.url_parameters, headers=self.url_headers)

        if self.response.status_code == 304:
            print("Forecast data has not been modified.")
        else:
            self.response.raise_for_status()
            print("Forecast has been modified.")

        self._json_from_response()
        self.save()
        self._parse_json()

    def intervals_for(self, day: dt.date) -> list:
        """Get intervals for specified day."""
        relevant_date = day
        relevant_intervals = []

        for interval in self.data["intervals"]:  # type: ignore
            if interval.start_time.date() == relevant_date:
                relevant_intervals.append(interval)

        return relevant_intervals

    def intervals_between(self, start: dt.datetime, end: dt.datetime) -> list:
        """Get intervals for specified day."""
        relevant_intervals = []

        for interval in self.data["intervals"]:  # type: ignore
            if start <= interval.start_time < end:
                relevant_intervals.append(interval)

        return relevant_intervals
