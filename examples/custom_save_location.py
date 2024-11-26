"""Using a custom save location.

Note there is now support for home directory ('~/') and relative notation ('../').
"""

import os
from metno_locationforecast import Place, Forecast

# Add your own user agent here.
USER_AGENT = "metno_locationforecast/2.0 https://github.com/Rory-Sullivan/metno-locationforecast"

new_york = Place("New York", 40.7, -74.0, 10)

# Provide a custom save location
new_york_forecast = Forecast(new_york, USER_AGENT, save_location="~/forecast_data/")

# Here we can view the actual save location
save_location = str(new_york_forecast.save_location)
print(save_location)

# Update the forecast. This requests data from the MET API and saves data to the
# save location.
new_york_forecast.update()

print(os.listdir(save_location))
