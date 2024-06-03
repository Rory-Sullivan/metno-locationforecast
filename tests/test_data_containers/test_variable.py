"""Tests for the Variable Class."""

import pytest

from metno_locationforecast.data_containers import Variable


def test_repr():
    temperature = Variable("temperature", 13.5, "celsius")

    assert repr(temperature) == "Variable(temperature, 13.5, celsius)"


def test_str():
    temperature = Variable("temperature", 13.5, "celsius")

    assert str(temperature) == "temperature: 13.5celsius"


def test_eq():
    temp1 = Variable("temperature", 13.5, "celsius")
    temp2 = Variable("temperature", 13.5, "celsius")
    temp3 = Variable("temperature", 10, "celsius")
    wind1 = Variable("wind_speed", 13.5, "m/s")
    temp_fahrenheit = Variable("temperature", 13.5, "fahrenheit")

    assert temp1 == temp2
    assert temp1 != temp3
    assert temp1 != wind1
    assert temp1 != temp_fahrenheit


def test_lt():
    temp1 = Variable("temperature", 13.5, "celsius")
    temp2 = Variable("temperature", 13.5, "celsius")
    temp3 = Variable("temperature", 15, "celsius")
    wind1 = Variable("wind_speed", 13.5, "m/s")
    temp_fahrenheit = Variable("temperature", 15, "fahrenheit")

    assert temp1 <= temp2  # type: ignore
    assert temp1 < 14
    assert temp1 < temp3
    assert temp3 > temp1
    with pytest.raises(TypeError):
        temp1 < wind1
    with pytest.raises(TypeError):
        temp1 < temp_fahrenheit


def test_add():
    temp1 = Variable("temperature", 2, "celsius")
    temp2 = Variable("temperature", 3, "celsius")
    temp3 = Variable("temperature", 10.5, "celsius")
    wind1 = Variable("wind_speed", 13.5, "m/s")
    temp_fahrenheit = Variable("temperature", 13.5, "fahrenheit")

    assert Variable("temperature", 5, "celsius") == temp1 + temp2
    assert Variable("temperature", 12.5, "celsius") == temp1 + temp3
    with pytest.raises(TypeError):
        temp1 + wind1
    with pytest.raises(TypeError):
        temp1 + temp_fahrenheit


def test_sub():
    temp1 = Variable("temperature", 2, "celsius")
    temp2 = Variable("temperature", 3, "celsius")
    temp3 = Variable("temperature", 10.5, "celsius")
    wind1 = Variable("wind_speed", 13.5, "m/s")
    temp_fahrenheit = Variable("temperature", 13.5, "fahrenheit")

    assert Variable("temperature", -1, "celsius") == temp1 - temp2
    assert Variable("temperature", -8.5, "celsius") == temp1 - temp3
    with pytest.raises(TypeError):
        temp1 - wind1
    with pytest.raises(TypeError):
        temp1 - temp_fahrenheit


def test_celsius_to_fahrenheit():
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


def test_mps_to_kph():
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


def test_mps_to_mph():
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


def test_mps_to_beaufort():
    zero = Variable("speed", 0, "m/s")
    slow = Variable("speed", 3, "m/s")
    fast = Variable("speed", 15.2, "m/s")
    error = Variable("", 0, "other")

    zero._mps_to_beaufort()
    slow._mps_to_beaufort()
    fast._mps_to_beaufort()

    assert zero.value == 0.0
    assert slow.value == 2.0
    assert fast.value == 7.0

    assert zero.units == "beaufort"

    with pytest.raises(ValueError):
        error._mps_to_beaufort()


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

    def test_converting_to_beaufort(self, ten_mps):
        ten_mps.convert_to("beaufort")

        assert ten_mps.value == 5.0
        assert ten_mps.units == "beaufort"

    def test_bad_conversion_raises_error(self, zero_celsius, ten_mps):
        with pytest.raises(ValueError):
            zero_celsius.convert_to("kp/h")

        with pytest.raises(ValueError):
            ten_mps.convert_to("fahrenheit")
