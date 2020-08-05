"""Classes for holding forecast data.

Classes:
    Place: Holds data for a place.
    Variable: Stores data for a weather variable.
    Interval: Stores information for an interval of a forecast.
    Data: Stores a complete collection of data
"""

import datetime as dt
from typing import Dict, List, Union, Optional


class Place:
    """Holds data for a place.

    Attributes:
        name: Name of place.
        coordinates (dict): Latitude (deg), longitude (deg) and altitude (metres).
    """

    def __init__(
        self,
        name: str,
        latitude: Union[float, int],
        longitude: Union[float, int],
        altitude: Optional[int] = None,
    ):
        """Create a Place object.

        Args:
            name: Name of the place.
            latitude: Latitude in degrees. Will be rounded to 4 decimals.
            longitude: Longitude in degrees. Will be rounded to 4 decimals.
            altitude: Optional; Alititute in metres. Will be rounded to an integer.
        """
        self.name = name
        self.coordinates: Dict[str, Union[float, int, None]] = {
            "latitude": round(latitude, 4),
            "longitude": round(longitude, 4),
        }
        if altitude is not None:
            self.coordinates["altitude"] = int(round(altitude, 0))
        else:
            self.coordinates["altitude"] = None

    def __repr__(self) -> str:
        return (
            f"Place({self.name}, {self.coordinates['latitude']}, {self.coordinates['longitude']}, "
            + f"altitude={self.coordinates['altitude']})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Place):
            return self.name == other.name and self.coordinates == other.coordinates
        return NotImplemented


class Variable:
    """Stores data for a weather variable.

    Also has a helpfull method for converting between units.

    Attributes:
        name: Name of the variable.
        value: Value of the variable.
        units: Units of the value of the variable.

    Methods:
        convert_to(units): Convert variable to given units.
    """

    VALID_UNIT_CONVERSIONS = {
        "m/s": {"km/h", "mph"},
        "celsius": {"fahrenheit"},
    }

    def __init__(self, name: str, value: Union[float, int], units: str):
        """Create Variable object.

        Args:
            name: The CF standard name of the variable.
            value: Value of the variable.
            units: Units of the variable as a string.
        """
        self.name = name
        self.value = value
        self.units = units

    def __repr__(self) -> str:
        return f"Variable({self.name}, {self.value}, {self.units})"

    def __str__(self) -> str:
        return f"{self.name}: {self.value}{self.units}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Variable):
            return (
                self.name == other.name and self.value == other.value and self.units == other.units
            )
        return NotImplemented

    def __add__(self, other: object) -> "Variable":
        if isinstance(other, Variable) and self.name == other.name and self.units == other.units:
            return Variable(self.name, self.value + other.value, self.units)
        return NotImplemented

    def __sub__(self, other: object) -> "Variable":
        if isinstance(other, Variable) and self.name == other.name and self.units == other.units:
            return Variable(self.name, self.value - other.value, self.units)
        return NotImplemented

    def _celsius_to_fahrenheit(self) -> None:
        """Convert from degrees Celsius to degrees Fahrenheit."""
        if self.units == "celsius":
            self.value = (((self.value / 5) * 9) + 32).__round__(2)
            self.units = "fahrenheit"
        else:
            msg = (
                "Not a valid unit conversion, expected units to be in 'celsius' but instead "
                + f"units were in {self.units}."
            )
            raise ValueError(msg)

    def _mps_to_kph(self) -> None:
        """Convert from metres per second to kilometres per hour."""
        if self.units == "m/s":
            self.units = "km/h"
            self.value = ((self.value * 360) / 100).__round__(2)
        else:
            msg = (
                "Not a valid unit conversion, expected units to be in 'm/s' but instead "
                + f"units were in {self.units}."
            )
            raise ValueError(msg)

    def _mps_to_mph(self) -> None:
        """Convert from metres per second to miles per hour."""
        if self.units == "m/s":
            self.units = "mph"
            self.value = (self.value * 2.236936).__round__(2)
        else:
            msg = (
                "Not a valid unit conversion, expected units to be in 'm/s' but instead "
                + f"units were in {self.units}."
            )
            raise ValueError(msg)

    def convert_to(self, units: str) -> None:
        """Convert variable to given units."""
        if self.units == units:
            return

        if units not in Variable.VALID_UNIT_CONVERSIONS[self.units]:
            msg = f"""Not a valid unit conversion. Valid destination units:
            {Variable.VALID_UNIT_CONVERSIONS[self.units]}"""
            raise ValueError(msg)

        if self.units == "celsius" and units == "fahrenheit":
            self._celsius_to_fahrenheit()
        elif self.units == "m/s" and units == "km/h":
            self._mps_to_kph()
        elif self.units == "m/s" and units == "mph":
            self._mps_to_mph()
        else:
            raise ValueError("Not a valid unit conversion.")


class Interval:
    """Stores information for an interval of a forecast.

    Attributes:
        start_time: Date and time of the start of the interval.
        end_time: Date and time of the end of the interval.
        symbol_code: String representing the appropriate icon from the Weather Icon service.
        variables: A dictionary of variables for the interval. Variables are indexed by their name.
    """

    def __init__(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
        symbol_code: str,
        variables: Dict[str, Variable],
    ):
        """Create an Interval object.

        Args:
            start_time: Date and time of the start of the interval.
            end_time: Date and time of the end of the interval.
            symbol_code: String representing the appropriate icon from the Weather Icon service.
            variables: A dictionary of variables for the interval. Variables should be indexed by
                their name.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.symbol_code = symbol_code
        self.variables = variables

    def __repr__(self) -> str:
        return f"Interval({self.start_time}, {self.end_time}, {self.symbol_code}, {self.variables})"

    def __str__(self) -> str:
        string = f"Forecast between {self.start_time} and {self.end_time}:"
        for variable in self.variables.values():
            string += f"\n\t{str(variable)}"
        return string

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Interval):
            return (
                self.start_time == other.start_time
                and self.end_time == other.end_time
                and self.symbol_code == other.symbol_code
                and self.variables == other.variables
            )
        return NotImplemented

    @property
    def duration(self) -> dt.timedelta:
        return self.end_time - self.start_time


class Data:
    """Class for storing a complete collection of data.

    Attributes:
        last_modified: Date and time the data was last modified
        expires: Date and time the data expires
        updated_at: Date and time the forecast was updated
        units: A dictionary mapping variable names to their units
        intervals: A chronological list of intervals in the data set

    Methods:
        intervals_for: Get intervals for a specific day
        intervals_between: Get intervals between a specific time period
    """

    def __init__(
        self,
        last_modified: dt.datetime,
        expires: dt.datetime,
        updated_at: dt.datetime,
        units: Dict[str, str],
        intervals: List[Interval],
    ):
        """Create a Data object.

        Args:
            last_modified: Date and time the data was last modified
            expires: Date and time the data expires
            updated_at: Date and time the forecast was updated
            units: A dictionary mapping variable names to their units
            intervals: A chronological list of intervals in the data set
        """
        self.last_modified = last_modified
        self.expires = expires
        self.updated_at = updated_at
        self.units = units
        self.intervals = intervals

    def __repr__(self) -> str:
        return (
            f"Data({self.last_modified}, {self.expires}, {self.updated_at}, {self.units}, "
            f"{self.intervals})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Data):
            return (
                self.last_modified == other.last_modified
                and self.expires == other.expires
                and self.updated_at == other.updated_at
                and self.units == other.units
                and self.intervals == other.intervals
            )
        return NotImplemented

    def intervals_for(self, day: dt.date) -> List[Interval]:
        """Return intervals for specified day."""
        relevant_intervals: List[Interval] = []

        for interval in self.intervals:
            if interval.start_time.date() == day:
                relevant_intervals.append(interval)

        return relevant_intervals

    def intervals_between(self, start: dt.datetime, end: dt.datetime) -> List[Interval]:
        """Return intervals between specified time periods."""
        relevant_intervals: List[Interval] = []

        for interval in self.intervals:
            if start <= interval.start_time < end:
                relevant_intervals.append(interval)

        return relevant_intervals
