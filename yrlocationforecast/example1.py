from yrlocationforecast import Place, Forecast


new_york = Place("New York", 40.7, -74.0, 10)
london = Place("London", 51.5, -0.1, 25)
beijing = Place("Beijing", 39.9, 116.4)

new_york_forecast = Forecast(
    new_york, "compact", "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
)
london_forecast = Forecast(
    london, "complete", "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
)
beijing_forecast = Forecast(
    beijing, "compact", "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
)

london_forecast.update()
new_york_forecast.update()
beijing_forecast.update()


# forecast.load()

# print(forecast.data["updated_at"])
# print(forecast.data["intervals"])
# print(forecast.data["expires"])
