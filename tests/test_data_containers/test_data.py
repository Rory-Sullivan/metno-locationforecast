"""Tests for the Data class."""

import datetime as dt

import pytest

from metno_locationforecast.data_containers import Place
from metno_locationforecast.forecast import Forecast

USER_AGENT = "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
SAVE_LOCATION = "./tests/test_data/"


@pytest.fixture
def new_york_data():
    lat = 40.7
    lon = -74.0
    alt = 10

    new_york = Place("New York", lat, lon, alt)

    new_york_forecast = Forecast(new_york, USER_AGENT, "compact", SAVE_LOCATION)
    new_york_forecast.load()

    return new_york_forecast.data


@pytest.fixture
def new_york_data_copy():
    lat = 40.7
    lon = -74.0
    alt = 10

    new_york = Place("New York", lat, lon, alt)

    new_york_forecast = Forecast(new_york, USER_AGENT, "compact", SAVE_LOCATION)
    new_york_forecast.load()

    return new_york_forecast.data


def test_eq(new_york_data, new_york_data_copy):
    assert new_york_data is not new_york_data_copy
    assert new_york_data == new_york_data_copy


def test_intervals_for(new_york_data):
    day = dt.date(year=2020, month=7, day=20)
    intervals = new_york_data.intervals_for(day)

    assert len(intervals) == 13
    assert intervals[12].variables["wind_speed"].value == 3.5


def test_intervals_between(new_york_data):
    start = dt.datetime(year=2020, month=7, day=20, hour=11)
    end = dt.datetime(year=2020, month=7, day=20, hour=15)
    intervals = new_york_data.intervals_between(start, end)

    assert len(intervals) == 4
    assert intervals[3].variables["wind_speed"].value == 4.4
