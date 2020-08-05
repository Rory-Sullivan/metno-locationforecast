"""Tests for data_containers.py."""

import datetime as dt

import pytest

from metno_locationforecast.data_containers import Interval, Place, Variable
from metno_locationforecast.forecast import Forecast


class TestPlace:
    """Tests for the Place class."""

    def test_altitude_attribute(self):
        """Test altitude attribute is initialised as expected."""
        with_altitude = Place("", 0.0, 0.0, 10)
        zero_altitude = Place("", 0.0, 0.0, 0)
        no_altitude = Place("", 0.0, 0.0)

        assert with_altitude.coordinates["altitude"] == 10
        assert zero_altitude.coordinates["altitude"] == 0
        assert no_altitude.coordinates["altitude"] is None

    def test_rounding(self):
        """Test rounding of attributes happens as appropriate."""
        no_rounding = Place("", 1.1111, 9.9999, 99)
        rounding = Place("", 1.11111, 9.99999, 99.9)

        assert no_rounding.coordinates == {"latitude": 1.1111, "longitude": 9.9999, "altitude": 99}
        assert rounding.coordinates == {"latitude": 1.1111, "longitude": 10.0, "altitude": 100}

    def test_repr(self):
        london = Place("London", 51.5, -0.1, 25)

        assert repr(london) == "Place(London, 51.5, -0.1, altitude=25)"


class TestVariable:
    """Tests for the Variable Class."""

    def test_repr(self):
        temperature = Variable("temperature", 13.5, "celsius")

        assert repr(temperature) == "Variable(temperature, 13.5, celsius)"

    def test_str(self):
        temperature = Variable("temperature", 13.5, "celsius")

        assert str(temperature) == "temperature: 13.5celsius"

    def test_celsius_to_fahrenheit(self):
        freezing = Variable("temperature", 0, "celsius")
        boiling = Variable("temperature", 100, "celsius")
        other = Variable("temperature", 37.5, "celsius")
        error = Variable("", 0, "other")

        freezing._celsius_to_fahrenheit()
        boiling._celsius_to_fahrenheit()
        other._celsius_to_fahrenheit()

        assert freezing.value == 32.0
        assert boiling.value == 212.0
        assert other.value == 99.5

        assert freezing.units == "fahrenheit"

        with pytest.raises(ValueError):
            error._celsius_to_fahrenheit()

    def test_mps_to_kph(self):
        zero = Variable("speed", 0, "m/s")
        slow = Variable("speed", 3, "m/s")
        fast = Variable("speed", 15.2, "m/s")
        error = Variable("", 0, "other")

        zero._mps_to_kph()
        slow._mps_to_kph()
        fast._mps_to_kph()

        assert zero.value == 0.0
        assert slow.value == 10.8
        assert fast.value == 54.72

        assert zero.units == "km/h"

        with pytest.raises(ValueError):
            error._mps_to_kph()

    def test_mps_to_mph(self):
        zero = Variable("speed", 0, "m/s")
        slow = Variable("speed", 3, "m/s")
        fast = Variable("speed", 15.2, "m/s")
        error = Variable("", 0, "other")

        zero._mps_to_mph()
        slow._mps_to_mph()
        fast._mps_to_mph()

        assert zero.value == 0.0
        assert slow.value == 6.71
        assert fast.value == 34.0

        assert zero.units == "mph"

        with pytest.raises(ValueError):
            error._mps_to_mph()

    class TestConvertTo:
        """Tests for the convert_to(units) method."""

        @pytest.fixture
        def zero_celsius(self):
            return Variable("temperature", 0, "celsius")

        @pytest.fixture
        def ten_mps(self):
            return Variable("speed", 10, "m/s")

        def test_no_convert(self, ten_mps):
            """Test that no conversion is made if the variable is already in the correct units."""
            ten_mps.convert_to("m/s")

            assert ten_mps.value == 10
            assert ten_mps.units == "m/s"

        def test_converting_to_fahrenheit(self, zero_celsius):
            zero_celsius.convert_to("fahrenheit")

            assert zero_celsius.value == 32.0
            assert zero_celsius.units == "fahrenheit"

        def test_converting_to_kph(self, ten_mps):
            ten_mps.convert_to("km/h")

            assert ten_mps.value == 36.0
            assert ten_mps.units == "km/h"

        def test_converting_to_mph(self, ten_mps):
            ten_mps.convert_to("mph")

            assert ten_mps.value == 22.37
            assert ten_mps.units == "mph"

        def test_bad_conversion_raises_error(self, zero_celsius, ten_mps):
            with pytest.raises(ValueError):
                zero_celsius.convert_to("kp/h")

            with pytest.raises(ValueError):
                ten_mps.convert_to("fahrenheit")


class TestInterval:
    """Tests for Interval class."""

    @pytest.fixture
    def generic_interval(self):
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

    def test_repr(self, generic_interval):
        expected = (
            "Interval(2020-01-01 12:00:00, 2020-01-01 16:00:00, cloudy, "
            + "{'temperature': Variable(temperature, 12.5, celsius), "
            + "'wind_speed': Variable(wind_speed, 3.2, m/s), "
            + "'wind_direction': Variable(wind_direction, 90, degrees)})"
        )

        assert repr(generic_interval) == expected

    def test_str(self, generic_interval):
        expected = """Forecast between 2020-01-01 12:00:00 and 2020-01-01 16:00:00:
\ttemperature: 12.5celsius
\twind_speed: 3.2m/s
\twind_direction: 90degrees"""

        assert str(generic_interval) == expected

    def test_duration(self, generic_interval):
        assert generic_interval.duration == dt.timedelta(hours=4)


class TestData:
    USER_AGENT = "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
    SAVE_LOCATION = "./tests/test_data/"

    @pytest.fixture
    def new_york_forecast(self):
        lat = 40.7
        lon = -74.0
        alt = 10

        new_york = Place("New York", lat, lon, alt)

        return Forecast(new_york, self.USER_AGENT, "compact", self.SAVE_LOCATION)

    def test_intervals_for(self, new_york_forecast):
        new_york_forecast.load()

        day = dt.date(year=2020, month=7, day=20)
        intervals = new_york_forecast.data.intervals_for(day)

        assert len(intervals) == 13
        assert intervals[12].variables["wind_speed"].value == 3.5

    def test_intervals_between(self, new_york_forecast):
        new_york_forecast.load()

        start = dt.datetime(year=2020, month=7, day=20, hour=11)
        end = dt.datetime(year=2020, month=7, day=20, hour=15)
        intervals = new_york_forecast.data.intervals_between(start, end)

        assert len(intervals) == 4
        assert intervals[3].variables["wind_speed"].value == 4.4
