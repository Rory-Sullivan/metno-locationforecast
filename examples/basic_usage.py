"""Basic usage."""

from yrlocationforecast import Place, Forecast

# Add your own user agent here.
USER_AGENT = "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"

new_york = Place("New York", 40.7, -74.0, 10)

new_york_forecast = Forecast(new_york, "compact", USER_AGENT)

new_york_forecast.update()

print(new_york_forecast)
