"""Tests the forecast class with various user configurations."""

import pytest
from metno_locationforecast.config import Config
from pathlib import Path
from metno_locationforecast.data_containers import Place


@pytest.fixture
def new_york():
    lat = 40.7
    lon = -74.0
    alt = 10

    return Place("New York", lat, lon, alt)


@pytest.fixture
def metno_locationforecast_config(monkeypatch):
    monkeypatch.setattr(
        Config, "cwd", Path("./tests/test_configs/test_metno_locationforecast_file/")
    )

    return Config()


@pytest.fixture
def no_user_config(monkeypatch):
    monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_no_config_file/"))

    return Config()


@pytest.fixture
def partial_config(monkeypatch):
    monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_partial_configuration/"))

    return Config()


def test_forecast_with_metno_locationforecast_file(metno_locationforecast_config, new_york):

    from metno_locationforecast import forecast

    forecast.CONFIG = metno_locationforecast_config

    f = forecast.Forecast(new_york)

    assert f.forecast_type == "metno_locationforecast_file"
    assert f.user_agent == "metno_locationforecast_file"
    assert f.save_location == Path("metno_locationforecast_file")
    assert f.base_url == "metno_locationforecast_file"


def test_forecast_with_no_config_file(no_user_config, new_york):

    from metno_locationforecast import forecast

    forecast.CONFIG = no_user_config

    f = forecast.Forecast(new_york, user_agent="test_user_agent")

    assert f.forecast_type == "compact"
    assert f.user_agent == "test_user_agent"
    assert f.save_location == Path("./data").resolve()
    assert f.base_url == "https://api.met.no/weatherapi/locationforecast/2.0/"


def test_forecast_raises_error_with_no_user_agent(no_user_config, new_york):

    from metno_locationforecast import forecast

    forecast.CONFIG = no_user_config

    with pytest.raises(ValueError):
        forecast.Forecast(new_york)


def test_forecast_with_partial_config_file(partial_config, new_york):

    from metno_locationforecast import forecast

    forecast.CONFIG = partial_config

    f = forecast.Forecast(new_york)

    assert f.forecast_type == "compact"
    assert f.user_agent == "setup_file"
    assert f.save_location == Path("./data").resolve()
    assert f.base_url == "https://api.met.no/weatherapi/locationforecast/2.0/"
