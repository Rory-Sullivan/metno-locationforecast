"""Tests for the Place class."""

from metno_locationforecast.data_containers import Place


def test_altitude_attribute():
    """Test altitude attribute is initialised as expected."""
    with_altitude = Place("", 0.0, 0.0, 10)
    zero_altitude = Place("", 0.0, 0.0, 0)
    no_altitude = Place("", 0.0, 0.0)

    assert with_altitude.coordinates["altitude"] == 10
    assert zero_altitude.coordinates["altitude"] == 0
    assert no_altitude.coordinates["altitude"] is None


def test_rounding():
    """Test rounding of attributes happens as appropriate."""
    no_rounding = Place("", 1.1111, 9.9999, 99)
    rounding = Place("", 1.11111, 9.99999, 99.9)

    assert no_rounding.coordinates == {"latitude": 1.1111, "longitude": 9.9999, "altitude": 99}
    assert rounding.coordinates == {"latitude": 1.1111, "longitude": 10.0, "altitude": 100}


def test_repr():
    london = Place("London", 51.5, -0.1, 25)

    assert repr(london) == "Place(London, 51.5, -0.1, altitude=25)"


def test_eq():
    place1 = Place("Dalkey Quarry", 53.271, -6.107, 95)
    place2 = Place("Dalkey Quarry", 53.271, -6.107, 95)
    place3 = Place("Dalkey Quarry", 53, -6.107, 95)
    place4 = Place("Dalkey Quarry", 53.271, -6.107, 96)
    not_a_place = "Dalkey Quarry"

    assert place1 == place2
    assert place1 != place3
    assert place1 != place4
    assert place1 != not_a_place
