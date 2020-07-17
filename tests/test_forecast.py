"""Tests for the forecast.py module."""

import pytest

from yrlocationforecast.forecast import Forecast
from yrlocationforecast.data_containers import Place

USER_AGENT = "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"


class TestForecast:
    """Tests for the Forecast class."""

    @pytest.fixture
    def new_york_forecast(self):
        lat = 40.7
        lon = -74.0
        alt = 10

        new_york = Place("New York", lat, lon, alt)

        return Forecast(new_york, "compact", USER_AGENT)

    @pytest.fixture
    def london_forecast(self):
        lat = 51.5
        lon = -0.1
        alt = 25

        london = Place("London", lat, lon, alt)

        return Forecast(london, "complete", USER_AGENT)

    @pytest.fixture
    def beijing_forecast(self):
        lat = 39.9
        lon = 116.4
        alt = 49

        beijing = Place("Beijing", lat, lon, alt)

        return Forecast(beijing, "compact", USER_AGENT)

    class TestInit:
        """Tests for the __init__ method."""

        def test_correct_usage(self, new_york_forecast):
            assert isinstance(new_york_forecast, Forecast)

        def test_place_parameter(self):
            place = "not a Place object"

            with pytest.raises(TypeError):
                Forecast(place, "compact", USER_AGENT)

        def test_forecast_type_parameter(self):
            lat = 40.7
            lon = -74.0
            alt = 10
            new_york = Place("New York", lat, lon, alt)

            type = "unsupported type"

            with pytest.raises(ValueError):
                Forecast(new_york, type, USER_AGENT)

    def test_repr(self, new_york_forecast):
        expect = (
            "Forecast(Place(New York, 40.7, -74.0, altitude=10), "
            + "compact, testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast, "
            + "save_location=data)"
        )
        assert repr(new_york_forecast) == expect
