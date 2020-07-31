"""Get forecast for a particular day."""

from metno_locationforecast import Place, Forecast
import datetime as dt

USER_AGENT = "metno_locationforecast/1.0 https://github.com/Rory-Sullivan/yrlocationforecast"
beijing = Place("Beijing", 39.9, 116.4)
beijing_forecast = Forecast(beijing, USER_AGENT)
beijing_forecast.update()

# Create a datetime.date object for the day in question.
tomorrow = dt.date.today() + dt.timedelta(days=1)

# Get intervals for that date.
tomorrows_intervals = beijing_forecast.intervals_for(tomorrow)

# Iterate through each of the returned intervals and print it.
print("Forecast for tomorrow in Beijing:\n")
for interval in tomorrows_intervals:
    print(interval)
