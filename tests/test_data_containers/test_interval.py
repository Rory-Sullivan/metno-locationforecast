"""Tests for Interval class."""

import datetime as dt

import pytest

from metno_locationforecast.data_containers import Interval, Variable


@pytest.fixture
def generic_interval():
    start = dt.datetime(year=2020, month=1, day=1, hour=12)
    end = dt.datetime(year=2020, month=1, day=1, hour=16)

    symbol_code = "cloudy"

    var1 = Variable("temperature", 12.5, "celsius")
    var2 = Variable("wind_speed", 3.2, "m/s")
    var3 = Variable("wind_direction", 90, "degrees")

    variables = {
        "temperature": var1,
        "wind_speed": var2,
        "wind_direction": var3,
    }

    return Interval(start, end, symbol_code, variables)


@pytest.fixture
def generic_interval_copy():
    start = dt.datetime(year=2020, month=1, day=1, hour=12)
    end = dt.datetime(year=2020, month=1, day=1, hour=16)

    symbol_code = "cloudy"

    var1 = Variable("temperature", 12.5, "celsius")
    var2 = Variable("wind_speed", 3.2, "m/s")
    var3 = Variable("wind_direction", 90, "degrees")

    variables = {
        "temperature": var1,
        "wind_speed": var2,
        "wind_direction": var3,
    }

    return Interval(start, end, symbol_code, variables)


def test_repr(generic_interval):
    expected = (
        "Interval(2020-01-01 12:00:00, 2020-01-01 16:00:00, cloudy, "
        + "{'temperature': Variable(temperature, 12.5, celsius), "
        + "'wind_speed': Variable(wind_speed, 3.2, m/s), "
        + "'wind_direction': Variable(wind_direction, 90, degrees)})"
    )

    assert repr(generic_interval) == expected


def test_str(generic_interval):
    expected = """Forecast between 2020-01-01 12:00:00 and 2020-01-01 16:00:00:
\ttemperature: 12.5celsius
\twind_speed: 3.2m/s
\twind_direction: 90degrees"""

    assert str(generic_interval) == expected


def test_eq(generic_interval, generic_interval_copy):
    assert generic_interval is not generic_interval_copy
    assert generic_interval == generic_interval_copy


def test_duration(generic_interval):
    assert generic_interval.duration == dt.timedelta(hours=4)
