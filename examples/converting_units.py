"""How to change units of certain variables."""

from yrlocationforecast import Place, Forecast

USER_AGENT = "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
london = Place("London", 51.5, -0.1, 25)
london_forecast = Forecast(london, "compact", USER_AGENT)
london_forecast.update()

for interval in london_forecast.data["intervals"]:
    for variable in interval.variables.values():
        if variable.name == "air_temperature":
            variable.convert_to("fahrenheit")
        elif variable.name == "wind_speed":
            variable.convert_to("mph")

print(london_forecast)
