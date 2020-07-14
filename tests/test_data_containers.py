"""Tests for data_containers.py."""

from yrlocationforecast.data_containers import Place, TempVariable, WindVariable, Interval, Forecast
import datetime as dt
import pytest


class TestPlace:
    @pytest.fixture
    def greenwich(self):
        return Place("Greenwich", 51.5, 0.0)

    @pytest.fixture
    def lug(self):
        return Place("Lugnaquilla", 52.96, -6.46, 905)

    def test_str(self, greenwich, lug):
        assert (
            str(greenwich) == "Place(name=Greenwich, latitude=51.5, longitude=0.0, altitude=None)"
        )
        assert str(lug) == "Place(name=Lugnaquilla, latitude=52.96, longitude=-6.46, altitude=905)"

    def test_repr(self, greenwich, lug):
        assert (
            repr(greenwich) == "Place(name=Greenwich, latitude=51.5, longitude=0.0, altitude=None)"
        )
        assert repr(lug) == "Place(name=Lugnaquilla, latitude=52.96, longitude=-6.46, altitude=905)"


class TestTempVariable:
    def test_str(self):
        temp = TempVariable(0.0, "celsius")

        assert str(temp) == "0.0℃"

        temp.celsius_to_fahrenheit()

        assert str(temp) == "32.0℉"

    def test_celsius_to_fahrenheit(self):
        temp_low = TempVariable(0, "celsius")
        temp_high = TempVariable(100, "celsius")
        temp_medium = TempVariable(47, "celsius")

        temp_low.celsius_to_fahrenheit()
        temp_high.celsius_to_fahrenheit()
        temp_medium.celsius_to_fahrenheit()

        assert temp_low.value == 32
        assert temp_low.unit == "fahrenheit"
        assert temp_high.value == 212
        assert temp_high.unit == "fahrenheit"
        assert round(temp_medium.value, 2) == 116.6
        assert temp_medium.unit == "fahrenheit"


class TestWindVariable:
    def test_str(self):
        wind = WindVariable(10.5, "mps", "west")

        assert str(wind) == "10.5mps west"

    def test_mps_to_kph(self):
        wind_zero = WindVariable(0.0, "mps", "")
        wind_slow = WindVariable(1.0, "mps", "")
        wind_medium = WindVariable(11.0, "mps", "")
        wind_fast = WindVariable(57.2, "mps", "")

        wind_zero.mps_to_kph()
        wind_slow.mps_to_kph()
        wind_medium.mps_to_kph()
        wind_fast.mps_to_kph()

        assert wind_zero.value == 0.0
        assert wind_zero.unit == "kph"
        assert wind_slow.value == 3.6
        assert wind_medium.value == 39.6
        assert wind_fast.value == 205.92


class TestForecast:
    def test_intervals_for(self):
        place = Place("Here", 0.0, 0.0)

        begin = dt.datetime(2020, 1, 1, 0, 0)

        delta_1_day = dt.timedelta(1, 0, 0)
        delta_6_hours = dt.timedelta(0, 21600, 0)

        day0 = begin.date()
        day1 = day0 + delta_1_day
        day2 = day1 + delta_1_day
        day3 = day2 + delta_1_day
        day4 = day3 + delta_1_day

        intervals = []
        for i in range(28):
            interval = Interval(begin + i * delta_6_hours, begin + (i + 1) * delta_6_hours, 0, {})
            intervals.append(interval)

        forecast = Forecast(place, begin, begin, intervals)

        day0_intervals = forecast.intervals_for(day0)
        day1_intervals = forecast.intervals_for(day1)
        day2_intervals = forecast.intervals_for(day2)
        day3_intervals = forecast.intervals_for(day3)
        day4_intervals = forecast.intervals_for(day4)

        assert len(day0_intervals) == 4
        assert day0_intervals[0] == intervals[0]
        assert day0_intervals[3] == intervals[3]

        assert len(day1_intervals) == 4
        assert day1_intervals[0] == intervals[4]
        assert day1_intervals[3] == intervals[7]

        assert len(day0_intervals) == 4
        assert day2_intervals[0] == intervals[8]
        assert day2_intervals[3] == intervals[11]

        assert len(day0_intervals) == 4
        assert day3_intervals[0] == intervals[12]
        assert day3_intervals[3] == intervals[15]

        assert len(day0_intervals) == 4
        assert day4_intervals[0] == intervals[16]
        assert day4_intervals[3] == intervals[19]
