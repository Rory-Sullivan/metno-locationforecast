"""Where the magic happens."""

import datetime as dt
import json
import os
from typing import Optional

import requests

from yrlocationforecast.data_containers import Interval, Place, Variable

YR_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Forecast:
    """Class for storing a forecast.  This is a group of forecast intervals."""

    base_url = "https://api.met.no/weatherapi/locationforecast/2.0/"
    forecast_types = {"classic", "commpact", "complete"}

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
        self.forecast_type = forecast_type

        self.user_agent = user_agent
        self.save_location = save_location

        self.response: Optional[requests.Response] = None
        self.json: Optional[dict] = None
        self.data: Optional[dict] = None

    def __repr__(self):
        return (
            f"Forecast(place={self.place}, forecast_type={self.forecast_type}, "
            + f"user_agent={self.user_agent}, save_location={self.save_location})"
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
            "user-agent": self.user_agent,
        }

        return headers

    def parse_json(self):
        json = self.json
        data = {}

        data["updated_at"] = dt.datetime.strptime(
            json["properties"]["meta"]["updated_at"], YR_DATETIME_FORMAT
        )

        data["units"] = json["properties"]["meta"]["units"]

        data["intervals"] = []
        for timeseries in json["properties"]["timeseries"]:
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

    def load(self):
        with open(self.save_location + self.file_name, "r") as f:
            self.json = json.loads(f.read())
        self.parse_json()

    def update(self):

        self.response = requests.get(self.url, params=self.url_parameters, headers=self.url_headers)
        self.response.raise_for_status()

        self.json = self.response.json()

        self.save()

        self.parse_json()

    @property
    def file_name(self):
        return (
            f"lat{self.place.coordinates['latitude']}lon{self.place.coordinates['longitude']}"
            + f"altitude{self.place.coordinates['altitude']}_{self.forecast_type}.json"
        )

    def save(self):
        if not os.path.exists(self.save_location):
            os.mkdir(self.save_location)

        with open(self.save_location + self.file_name, "w") as f:
            f.write(self.response.text)

    def intervals_for(self, day: dt.date) -> list:
        """Get intervals for specified day."""
        relevant_date = day
        relevant_intervals = []

        for interval in self.data["intervals"]:  # type: ignore
            if interval.start_time.date() == relevant_date:
                relevant_intervals.append(interval)

        return relevant_intervals
