"""Tests for the forecast.py module."""

import json
import datetime as dt

import pytest

from metno_locationforecast.data_containers import Place
from metno_locationforecast.forecast import Forecast

USER_AGENT = "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
SAVE_LOCATION = "./tests/test_data/"


class TestForecast:
    """Tests for the Forecast class."""

    @pytest.fixture
    def new_york_forecast(self):
        lat = 40.7
        lon = -74.0
        alt = 10

        new_york = Place("New York", lat, lon, alt)

        return Forecast(new_york, USER_AGENT, "compact", SAVE_LOCATION)

    @pytest.fixture
    def london_forecast(self):
        lat = 51.5
        lon = -0.1
        alt = 25

        london = Place("London", lat, lon, alt)

        return Forecast(london, USER_AGENT, "complete", SAVE_LOCATION)

    @pytest.fixture
    def beijing_forecast(self):
        lat = 39.9
        lon = 116.4

        beijing = Place("Beijing", lat, lon)

        base_url = "somewhere.com/met-api/"

        return Forecast(beijing, USER_AGENT, "compact", SAVE_LOCATION, base_url)

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

        def test_forecast_type_with_custom_url(self):
            lat = 40.7
            lon = -74.0
            alt = 10
            new_york = Place("New York", lat, lon, alt)

            type = ""
            base_url = "custom-domain.com/"

            forecast = Forecast(new_york, USER_AGENT, type, base_url=base_url)

            assert isinstance(forecast, Forecast)
            assert forecast.url == "custom-domain.com/"

    def test_repr(self, new_york_forecast):
        expect = (
            "Forecast(Place(New York, 40.7, -74.0, altitude=10), "
            + "compact, testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast, "
            + "save_location=tests\\test_data)"
        )
        assert repr(new_york_forecast) == expect

    def test_url_property(self, new_york_forecast, london_forecast, beijing_forecast):
        assert new_york_forecast.url == "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        assert london_forecast.url == "https://api.met.no/weatherapi/locationforecast/2.0/complete"
        assert beijing_forecast.url == "somewhere.com/met-api/compact"

    def test_url_parameters_property(self, new_york_forecast, beijing_forecast):
        new_york_parameters = {
            "lat": 40.7,
            "lon": -74.0,
            "altitude": 10,
        }
        beijing_parameters = {
            "lat": 39.9,
            "lon": 116.4,
        }

        assert new_york_forecast.url_parameters == new_york_parameters
        assert beijing_forecast.url_parameters == beijing_parameters

    def test_url_headers_property(self, new_york_forecast, london_forecast):
        new_york_headers = {
            "User-Agent": "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast",
        }

        london_forecast.load()
        london_headers = {
            "User-Agent": "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast",
            "If-Modified-Since": "Mon, 20 Jul 2020 11:44:31 GMT",
        }

        assert new_york_forecast.url_headers == new_york_headers
        assert london_forecast.url_headers == london_headers

    def test_filename_property(self, new_york_forecast, london_forecast, beijing_forecast):
        new_york_filename = "lat40.7lon-74.0altitude10_compact.json"
        london_filename = "lat51.5lon-0.1altitude25_complete.json"
        beijing_filename = "lat39.9lon116.4altitudeNone_compact.json"

        assert new_york_forecast.file_name == new_york_filename
        assert london_forecast.file_name == london_filename
        assert beijing_forecast.file_name == beijing_filename

    class TestJsonFromResponse:
        """Tests for the _json_from_response() method."""

        def test_response_200(self, mock_200_response, new_york_forecast):
            new_york_forecast.response = mock_200_response
            new_york_forecast._json_from_response()

            expected_json_string = f'{{"status_code":{mock_200_response.status_code},"headers":{json.dumps(mock_200_response.headers)},"data":{mock_200_response.text}}}'  # noqa: E501
            expected_json = json.loads(expected_json_string)

            assert new_york_forecast.json_string == expected_json_string
            assert new_york_forecast.json == expected_json

        def test_response_304(self, mock_304_response, new_york_forecast):
            new_york_forecast.load()
            new_york_forecast.response = mock_304_response
            new_york_forecast._json_from_response()

            with open("./tests/test_data/lat40.7lon-74.0altitude10_compact.json", "r") as f:
                data = f.read()
            data = json.dumps(json.loads(data)["data"])

            expected_json_string = f'{{"status_code":{mock_304_response.status_code},"headers":{json.dumps(mock_304_response.headers)},"data":{data}}}'  # noqa: E501
            expected_json = json.loads(expected_json_string)

            assert new_york_forecast.json == expected_json

    def test_parse_json(self, new_york_forecast):
        with open("./tests/test_data/lat40.7lon-74.0altitude10_compact.json", "r") as f:
            _json = json.load(f)

        new_york_forecast.json = _json
        new_york_forecast._parse_json()

        expected_last_modified = dt.datetime(
            year=2020, month=7, day=20, hour=11, minute=44, second=31
        )
        expected_units_of_temperature = "celsius"
        expected_first_interval_start = dt.datetime(year=2020, month=7, day=20, hour=11)
        expected_first_interval_end = dt.datetime(year=2020, month=7, day=20, hour=12)
        expected_first_interval_rain = 0.0

        assert new_york_forecast.data.last_modified == expected_last_modified
        assert new_york_forecast.data.units["air_temperature"] == expected_units_of_temperature
        assert new_york_forecast.data.intervals[0].start_time == expected_first_interval_start
        assert new_york_forecast.data.intervals[0].end_time == expected_first_interval_end
        assert (
            new_york_forecast.data.intervals[0].variables["precipitation_amount"].value
            == expected_first_interval_rain
        )

    class TestDataOutdated:
        """Tests for the _data_outdated method."""

        def test_in_date(self, mock_in_date, new_york_forecast):
            new_york_forecast.load()
            assert new_york_forecast._data_outdated() is False

        def test_out_of_date(self, mock_out_of_date, new_york_forecast):
            new_york_forecast.load()
            assert new_york_forecast._data_outdated() is True

    class TestSave:
        """Tests for the save method."""

        def test_save_to_existing_dir(self, tmp_path, new_york_forecast):
            new_york_forecast.load()

            new_location = tmp_path.joinpath("new_data/")
            new_location.mkdir()
            new_york_forecast.save_location = new_location

            new_york_forecast.save()

            file = tmp_path.joinpath("new_data/lat40.7lon-74.0altitude10_compact.json")
            assert file.exists()
            assert file.is_file()

        def test_save_to_nonexisting_dir(self, tmp_path, new_york_forecast):
            new_york_forecast.load()

            new_location = tmp_path.joinpath("new_data/")
            new_york_forecast.save_location = new_location

            new_york_forecast.save()

            file = tmp_path.joinpath("new_data/lat40.7lon-74.0altitude10_compact.json")
            assert file.exists()
            assert file.is_file()

        def test_throw_error_when_not_a_dir(self, tmp_path, new_york_forecast):
            new_path = tmp_path.joinpath("new_data")
            new_path.touch()

            new_york_forecast.save_location = new_path

            with pytest.raises(NotADirectoryError):
                new_york_forecast.save()

    class TestLoad:
        """Tests for the load method."""

        def test_load_new_york_data(self, new_york_forecast):
            new_york_forecast.load()

            with open("./tests/test_data/lat40.7lon-74.0altitude10_compact.json", "r") as f:
                expected_json_string = f.read()

            assert new_york_forecast.json_string == expected_json_string

    class TestUpdate:
        """Tests for the update method."""

        def test_data_in_date(self, tmp_path, mock_in_date, new_york_forecast):
            new_york_forecast.load()
            new_york_forecast.save_location = tmp_path

            update_return = new_york_forecast.update()

            assert update_return == "Data-Not-Expired"

        def test_data_outdated_and_not_modified(
            self, tmp_path, mock_out_of_date, mock_304_request, new_york_forecast
        ):
            new_york_forecast.load()
            new_york_forecast.save_location = tmp_path

            update_return = new_york_forecast.update()

            assert update_return == "Data-Not-Modified"

        def test_data_outdated_and_modified(
            self, tmp_path, mock_out_of_date, mock_200_request, new_york_forecast
        ):
            new_york_forecast.load()
            new_york_forecast.save_location = tmp_path

            update_return = new_york_forecast.update()

            assert update_return == "Data-Modified"

        def test_no_data(self, tmp_path, mock_out_of_date, mock_200_request, new_york_forecast):
            new_york_forecast.save_location = tmp_path

            update_return = new_york_forecast.update()

            assert update_return == "Data-Modified"

    def test_intervals_for(self, new_york_forecast):
        new_york_forecast.load()

        day = dt.date(year=2020, month=7, day=20)
        intervals = new_york_forecast.intervals_for(day)

        assert len(intervals) == 13
        assert intervals[12].variables["wind_speed"].value == 3.5

    def test_intervals_between(self, new_york_forecast):
        new_york_forecast.load()

        start = dt.datetime(year=2020, month=7, day=20, hour=11)
        end = dt.datetime(year=2020, month=7, day=20, hour=15)
        intervals = new_york_forecast.intervals_between(start, end)

        assert len(intervals) == 4
        assert intervals[3].variables["wind_speed"].value == 4.4
