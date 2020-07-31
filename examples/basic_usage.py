"""Basic usage."""

from metno_locationforecast import Place, Forecast

# Add your own user agent here.
USER_AGENT = "metno_locationforecast/1.0 https://github.com/Rory-Sullivan/yrlocationforecast"

# Create a Place instance.
# Place(name, latitude, longitude, altitude)
new_york = Place("New York", 40.7, -74.0, 10)

# Create a Forecast instance for the place.
# Forecast(place, forecast_type, user_agent, save_location="./data/")
new_york_forecast = Forecast(new_york, "compact", USER_AGENT)

# Update the forecast. This requests data from the MET API and saves data to the
# save location.
new_york_forecast.update()

print(new_york_forecast)
