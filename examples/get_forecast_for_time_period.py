"""Get forecast for a particular time period (e.g. tomorrow afternoon)."""

import datetime as dt
from zoneinfo import ZoneInfo

from metno_locationforecast import Forecast, Place

# Add your own user agent here.
USER_AGENT = "metno_locationforecast/2.0 https://github.com/Rory-Sullivan/metno-locationforecast"

seattle = Place("Seattle", 47.605, -122.330)
seattle_forecast = Forecast(seattle, USER_AGENT)
seattle_forecast.update()

# Create the time interval in question. Note the timezone info is recommended
# for localised results.
tomorrow = dt.date.today() + dt.timedelta(days=1)
timezone = ZoneInfo("America/Los_Angeles")
tomorrow_afternoon_start = dt.datetime.combine(
    tomorrow, dt.time(hour=12, minute=0, tzinfo=timezone)
)
tomorrow_afternoon_end = dt.datetime.combine(
    tomorrow + dt.timedelta(days=1), dt.time(hour=0, minute=0, tzinfo=timezone)
)

# Get intervals for that time interval.
tomorrows_intervals = seattle_forecast.data.intervals_between(
    tomorrow_afternoon_start, tomorrow_afternoon_end
)

# Iterate through each of the returned intervals and print it.
print("Forecast for tomorrow afternoon in Seattle:\n")
for interval in tomorrows_intervals:
    print(interval)
