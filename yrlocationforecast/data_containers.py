"""Classes for holding forecast data."""

import datetime as dt


class Place:
    """Holds data for a place."""

    def __init__(self, name: str, latitude: float, longitude: float, altitude: int = None):
        self.name = name
        self.coordinates = {
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
        }

    def __repr__(self):
        return (
            f"Place(name={self.name}, latitude={self.coordinates['latitude']}, "
            + f"longitude={self.coordinates['longitude']}, "
            + f"altitude={self.coordinates['altitude']})"
        )


class Variable:
    """Stores data for weather variable."""

    def __init__(self, variable: str, value: float, unit: str):
        self.variable = variable
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"Variable(variable={self.variable}, value={self.value}, unit={self.unit})"

    def __str__(self):
        return f"{self.value}{self.unit}"


class TempVariable(Variable):
    """Stores temperature data."""

    def __repr__(self):
        return f"TempVariable(variable={self.variable}, value={self.value}, unit={self.unit})"

    def __str__(self):
        if self.unit == "celsius":
            return f"{self.value}℃"
        if self.unit == "fahrenheit":
            return f"{self.value}℉"
        return super().__str__()

    def celsius_to_fahrenheit(self):
        if self.unit == "celsius":
            self.value = ((self.value / 5) * 9) + 32
            self.unit = "fahrenheit"

        elif self.unit == "fahrenheit":
            pass

        else:
            raise ValueError(
                "Not a valid unit conversion, units must be 'celsius' or 'fahrenheit'."
            )


class WindVariable(Variable):
    """Special variable class for storing wind data."""

    def __init__(self, variable: str, value: float, unit: str, direction: str):
        self.direction = direction
        super().__init__(variable, value, unit)

    def __repr__(self):
        return (
            f"WindVariable(variable={self.variable}, value={self.value}, unit={self.unit}, "
            + f"direction={self.direction})"
        )

    def __str__(self):
        return f"{self.value}{self.unit} {self.direction}"

    def mps_to_kph(self):
        """Convert from metres per second to kilometres per hour."""
        if self.unit == "mps":
            self.unit = "kph"
            self.value = ((self.value * 360) / 100).__round__(2)

        elif self.unit == "kph":
            pass

        else:
            raise ValueError("Not a valid unit conversion units must be 'mps' or 'kph'.")


class Interval:
    """Stores information for an interval of a forecast, contains variables."""

    def __init__(
        self, start_time: dt.datetime, end_time: dt.datetime, symbol_code: str, variables: dict
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.symbol_code = symbol_code
        self.variables = variables

    def __repr__(self):
        return (
            f"ForecastInterval(start_time={self.start_time}, end_time={self.end_time}, "
            + f"symbol_code={self.symbol_code}, variables={self.variables})"
        )

    def __str__(self):
        string = f"Forecast between: {self.start_time} and {self.end_time}"
        for variable in self.variables_dict.values():
            string += f"\n{str(variable)}"
        return string

    @property
    def duration(self):
        return self.end_time - self.start_time


class Forecast:
    """Class for storing a forecast.  This is a group of forecast intervals."""

    def __init__(
        self, place: Place, updated_at: dt.datetime, valid_until: dt.datetime, intervals: list,
    ):
        self.place = place
        self.updated_at = updated_at
        self.valid_until = valid_until
        self.intervals = intervals

    def __repr__(self):
        return (
            f"Forecast(place={self.place}, updated_at={self.updated_at}, "
            + f"valid_until={self.valid_until}, intervals={self.forecat_intervals})"
        )

    def intervals_for(self, day: dt.date) -> list:
        """Get intervals for specified day."""
        relevant_date = day
        relevant_intervals = []

        for interval in self.intervals:
            if interval.start_time.date() == relevant_date:
                relevant_intervals.append(interval)

        return relevant_intervals
