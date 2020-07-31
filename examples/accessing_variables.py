"""An example of accessing individual forecast variables."""

from metno_locationforecast import Place, Forecast

USER_AGENT = "metno_locationforecast/1.0 https://github.com/Rory-Sullivan/yrlocationforecast"

new_york = Place("New York", 40.7, -74.0, 10)
new_york_forecast = Forecast(new_york, "compact", USER_AGENT)
new_york_forecast.update()

# Access a particular interval.
first_interval = new_york_forecast.data.intervals[0]
print(first_interval)

# Access the interval's duration attribute.
print(f"Duration: {first_interval.duration}")

print()  # Blank line

# Access a particular variable from the interval.
rain = first_interval.variables["precipitation_amount"]
print(rain)

# Access the variables value and unit attributes.
print(f"Rain value: {rain.value}")
print(f"Rain units: {rain.units}")

# Get a full list of variables available in the interval.
print(first_interval.variables.keys())
