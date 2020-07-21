"""Get forecast for tomorrow."""

from yrlocationforecast import Place, Forecast
import datetime as dt

beijing = Place("Beijing", 39.9, 116.4)
beijing_forecast = Forecast(
    beijing, "compact", "testing/0.1 https://github.com/Rory-Sullivan/yrlocationforecast"
)
beijing_forecast.update()

tomorrow = dt.date.today() + dt.timedelta(days=1)

tomorrows_intervals = beijing_forecast.intervals_for(tomorrow)

print("Forecast for tomorrow in Beijing:\n")

for interval in tomorrows_intervals:
    print(interval)
