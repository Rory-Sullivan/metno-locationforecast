"""Classes and functions used for mocking responses from the requests library."""

import datetime as dt
import json

import pytest
import requests


class MockResponse:
    """Mock requests.response class."""

    def __init__(self, status_code: int, headers: dict, text: str):
        self.status_code = status_code
        self.headers = headers
        self.text = text

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        pass


@pytest.fixture
def mock_200_response():
    status_code = 200
    headers = {
        "Expires": "Mon, 20 Jul 2020 12:14:53 GMT",
        "Last-Modified": "Mon, 20 Jul 2020 11:44:31 GMT",
    }
    text = """{"properties":{"meta":{"updated_at":"2020-07-20T01:30:57Z","units":{"air_temperature":"celsius","precipitation_amount":"mm","wind_from_direction":"degrees","wind_speed":"m/s"}},"timeseries":[{"time":"2020-07-20T11:00:00Z","data":{"instant":{"details":{"air_temperature":26.5,"wind_from_direction":243.4,"wind_speed":3.8}},"next_1_hours":{"summary":{"symbol_code":"partlycloudy_day"},"details":{"precipitation_amount":0.0}}}}]}}"""  # noqa: E501

    return MockResponse(status_code, headers, text)


@pytest.fixture
def mock_304_response():
    status_code = 304
    headers = {
        "Expires": "Mon, 20 Jul 2020 12:14:53 GMT",
        "Last-Modified": "Mon, 20 Jul 2020 11:44:31 GMT",
    }
    text = ""

    return MockResponse(status_code, headers, text)


@pytest.fixture
def mock_200_request(monkeypatch):
    status_code = 200
    headers = {
        "Expires": "Mon, 20 Jul 2020 12:14:53 GMT",
        "Last-Modified": "Mon, 20 Jul 2020 11:44:31 GMT",
    }
    text = """{"properties":{"meta":{"updated_at":"2020-07-20T01:30:57Z","units":{"air_temperature":"celsius","precipitation_amount":"mm","wind_from_direction":"degrees","wind_speed":"m/s"}},"timeseries":[{"time":"2020-07-20T11:00:00Z","data":{"instant":{"details":{"air_temperature":26.5,"wind_from_direction":243.4,"wind_speed":3.8}},"next_1_hours":{"summary":{"symbol_code":"partlycloudy_day"},"details":{"precipitation_amount":0.0}}}}]}}"""  # noqa: E501

    def mock_request(*args, **kwargs):
        return MockResponse(status_code, headers, text)

    monkeypatch.setattr(requests, "get", mock_request)


@pytest.fixture
def mock_304_request(monkeypatch):
    status_code = 304
    headers = {
        "Expires": "Mon, 20 Jul 2020 12:14:53 GMT",
        "Last-Modified": "Mon, 20 Jul 2020 11:44:31 GMT",
    }
    text = ""

    def mock_request(*args, **kwargs):
        return MockResponse(status_code, headers, text)

    monkeypatch.setattr(requests, "get", mock_request)


@pytest.fixture
def mock_in_date(monkeypatch):
    indate_date = dt.datetime(year=2020, month=7, day=20, hour=12, minute=13, second=0)

    class MockDatetime:
        strptime = dt.datetime.strptime

        @classmethod
        def utcnow(cls):
            return indate_date

    monkeypatch.setattr(dt, "datetime", MockDatetime)


@pytest.fixture
def mock_out_of_date(monkeypatch):
    outdate_date = dt.datetime(year=2020, month=7, day=20, hour=12, minute=15, second=0)

    class MockDatetime:
        strptime = dt.datetime.strptime

        @classmethod
        def utcnow(cls):
            return outdate_date

    monkeypatch.setattr(dt, "datetime", MockDatetime)
