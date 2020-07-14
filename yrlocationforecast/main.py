from yrlocationforecast.data_containers import Place
from yrlocationforecast.forecasts import Forecast

greenwich = Place("Greenwich", 51.5, 0.0)

forecast = Forecast(greenwich, "compact", "Testing/0.1")

forecast.load()

print(forecast.data["updated_at"])
print(forecast.data["intervals"])
