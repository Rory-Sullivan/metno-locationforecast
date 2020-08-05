"""Tests for the config.py module."""

from pathlib import Path

import pytest

from metno_locationforecast.config import Config


class TestConfig:
    class TestPossibleUserConfigFiles:
        def test_metno_locationforecast_file(self, monkeypatch):
            monkeypatch.setattr(
                Config, "cwd", Path("./tests/test_configs/test_metno_locationforecast_file/")
            )

            config = Config()

            result = list(config.possible_user_config_files)

            expected = [
                Path(
                    "./tests/test_configs/test_metno_locationforecast_file/"
                    "metno-locationforecast.ini"
                )
            ]

            assert result == expected

        def test_setup_file(self, monkeypatch):
            monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_setup_file/"))

            config = Config()

            result = list(config.possible_user_config_files)

            expected = [Path("./tests/test_configs/test_setup_file/setup.cfg")]

            assert result == expected

        def test_multiple_files(self, monkeypatch):
            monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_multiple_files/"))

            config = Config()

            result = list(config.possible_user_config_files)

            expected = [
                Path("./tests/test_configs/test_multiple_files/metno-locationforecast.ini"),
                Path("./tests/test_configs/test_multiple_files/setup.cfg"),
            ]

            assert result == expected

        def test_no_files(self, monkeypatch):
            monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_no_config_file/"))

            config = Config()

            result = list(config.possible_user_config_files)

            expected = []

            assert result == expected

    class TestInit:
        def test_metno_locationforecast_file(self, monkeypatch):
            monkeypatch.setattr(
                Config, "cwd", Path("./tests/test_configs/test_metno_locationforecast_file/")
            )

            config = Config()

            assert config.forecast_type == "metno_locationforecast_file"
            assert config.user_agent == "metno_locationforecast_file"
            assert config.save_location == "metno_locationforecast_file"
            assert config.base_url == "metno_locationforecast_file"
            assert config.user_config_file == str(
                Path(
                    "./tests/test_configs/test_metno_locationforecast_file/metno-locationforecast.ini"
                ).resolve()
            )

        def test_setup_file(self, monkeypatch):
            monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_setup_file/"))

            config = Config()

            assert config.forecast_type == "setup_file"
            assert config.user_agent == "setup_file"
            assert config.save_location == "setup_file"
            assert config.base_url == "setup_file"
            assert config.user_config_file == str(
                Path("./tests/test_configs/test_setup_file/setup.cfg").resolve()
            )

        def test_precedence_of_files(self, monkeypatch):
            monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_multiple_files/"))

            config = Config()

            assert config.forecast_type == "metno_locationforecast_file"
            assert config.user_agent == "metno_locationforecast_file"
            assert config.save_location == "metno_locationforecast_file"
            assert config.base_url == "metno_locationforecast_file"
            assert config.user_config_file == str(
                Path(
                    "./tests/test_configs/test_multiple_files/metno-locationforecast.ini"
                ).resolve()
            )

        def test_no_files(self, monkeypatch):
            monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_no_config_file/"))

            config = Config()

            assert config.forecast_type == "compact"
            assert config.user_agent is None
            assert config.save_location == "./data"
            assert config.base_url == "https://api.met.no/weatherapi/locationforecast/2.0/"
            assert config.user_config_file is None

        def test_partial_configuration(self, monkeypatch):
            monkeypatch.setattr(
                Config, "cwd", Path("./tests/test_configs/test_partial_configuration/")
            )

            config = Config()

            assert config.forecast_type == "compact"
            assert config.user_agent == "setup_file"
            assert config.save_location == "./data"
            assert config.base_url == "https://api.met.no/weatherapi/locationforecast/2.0/"
            assert config.user_config_file == str(
                Path("./tests/test_configs/test_partial_configuration/setup.cfg").resolve()
            )

        def test_bad_configuration(self, monkeypatch):
            monkeypatch.setattr(Config, "cwd", Path("./tests/test_configs/test_bad_config_file/"))

            with pytest.warns(UserWarning):
                config = Config()

            assert config.forecast_type == "setup_file"
            assert config.user_agent == "setup_file"
            assert config.save_location == "./data"
            assert config.base_url == "https://api.met.no/weatherapi/locationforecast/2.0/"
            assert config.user_config_file == str(
                Path("./tests/test_configs/test_bad_config_file/setup.cfg").resolve()
            )
            assert not hasattr(config, "not_a_real_configuration")
