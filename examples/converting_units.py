"""How to change the units of certain variables."""

from metno_locationforecast import Place, Forecast

# Add your own user agent here.
USER_AGENT = "metno_locationforecast/2.0 https://github.com/Rory-Sullivan/metno-locationforecast"

london = Place("London", 51.5, -0.1, 25)
london_forecast = Forecast(london, USER_AGENT)
london_forecast.update()

# Iterate over all variables of every interval.
for interval in london_forecast.data.intervals:
    for variable in interval.variables.values():

        # Change temperature units to Fahrenheit
        if variable.name == "air_temperature":
            variable.convert_to("fahrenheit")

        # Change wind speed units to miles per hour.
        elif variable.name == "wind_speed":
            variable.convert_to("mph")

# Print forecast, notice the new variables.
print(london_forecast)
