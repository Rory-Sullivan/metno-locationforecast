"""Get forecast for a particular day."""

import datetime as dt
from zoneinfo import ZoneInfo

from metno_locationforecast import Forecast, Place

# Add your own user agent here.
USER_AGENT = "metno_locationforecast/2.0 https://github.com/Rory-Sullivan/metno-locationforecast"

beijing = Place("Beijing", 39.9, 116.4)
beijing_forecast = Forecast(beijing, USER_AGENT)
beijing_forecast.update()

# Create a datetime.date object for the day in question.
tomorrow = dt.date.today() + dt.timedelta(days=1)

# Create a timezone object for the correct timezone, this is optional but is
# best for localised results
timezone = ZoneInfo("Asia/Shanghai")

# Get intervals for that date.
tomorrows_intervals = beijing_forecast.data.intervals_for(tomorrow, timezone)

# Iterate through each of the returned intervals and print it.
print("Forecast for tomorrow in Beijing:\n")
for interval in tomorrows_intervals:
    print(interval)
