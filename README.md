# MET Norway Location Forecast

A Python interface for the MET Norway
[Locationforecast/2.0](https://api.met.no/weatherapi/locationforecast/2.0/documentation)
service. This is a free weather data service provided by the [Norwegian
Meteorological Institute](https://www.met.no/en).

## Contents

- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
  - [Basics](#Basics)
  - [Accessing Data](#Accessing-Data)
  - [Custom URLs](#Custom-URLs)
  - [Configuration](#Configuration)
  - [More Examples](#More-Examples)
- [Notes on Licensing](#Notes-on-Licensing)
- [Dependencies](#Dependencies)
- [Useful Links](#Useful-Links)

## Features

- Get weather data for anywhere in the world
- Automatically take care of caching data
- Helpful classes for managing forecast data
- Convert between units of measurement

## Installation

Installing with pip:

```shell
pip install metno-locationforecast
```

It's recommended to install ```metno-locationforecast``` into a virtual
environment for your application.

## Usage

### Basics

Before using this package you should be aware of the [terms of
service](https://api.met.no/doc/TermsOfService) for using the MET Weather API.

The ```metno-locationforecast``` package will not make requests unless current
data has expired and will send requests with the appropriate
```If-Modified-Since``` header where possible. Identification can be provided by
passing a ```User-Agent``` string to the forecast class, see more on this below.

After installing ```metno-locationforecast``` the following commands can be run
in a python console. Start by importing the ```Place``` and ```Forecast```
classes, these are the main classes you will need to interact with.

```pycon
>>> from metno_locationforecast import Place, Forecast
```

**Note:** Use an underscore in the name when importing.

Create a ```Place``` instance. The first argument is your name for the place,
next are the geographic coordinates. Geographic coordinates are given by
latitude, longitude (in degrees) and altitude (in metres).

```pycon
>>> new_york = Place("New York", 40.7, -74.0, 10)
```

The altitude parameter is optional but recommended. Note that latitude and
longitude are rounded to four decimal places and altitude is rounded to the
nearest integer, this is required by the MET API.
[GeoNames](http://www.geonames.org/) is a helpful website for finding the
geographic coordinates of a place.

Next create a ```Forecast``` instance for the place. Here you need to supply a
```User-Agent``` string, typically this will include the name and version of
your application as well as contact information (email address or website) more
details on what is expected [here](https://api.met.no/doc/TermsOfService). Do
NOT use the string supplied here as this does not apply to your site.

```pycon
>>> ny_forecast = Forecast(new_york, "metno-locationforecast/1.0 https://github.com/Rory-Sullivan/metno-locationforecast")
```

There are also three optional arguments that you can supply. First is the
```forecast_type``` parameter, options are ```"compact"``` (a limited set of
variables suitable for most purposes) or ```"complete"``` (an extensive set of
weather data). For more details on the differences check out the this
[page](https://api.met.no/doc/locationforecast/datamodel). ```"compact"``` is
the default.

The second optional parameter is ```save_location```, this is the folder where
data will be stored. The default is ```"./data/"```. Finally there is the
```base_url``` parameter, more on this in the [Custom URLs](#Custom-URLs)
section.

These parameters can be configured for your entire app by using a configuration
file, more on this in the [configuration](#Configuration) section.

Next run the update method. This will make a request to the MET API for data and
will save the data to the save location. If data already exists for the
forecast, this will only request new data if the data has expired and will make
the request using the appropriate ```If-Modified-Since``` header. It returns a
string describing which process occurred, this will be one of
```'Data-Not-Expired'```, ```'Data-Not-Modified'``` or ```'Data-Modified'```.
Only in the case of ```'Data-Modified'``` has any change to the data occurred.

```pycon
>>> ny_forecast.update()
'Data-Modified'
>>> ny_forecast.update()
'Data-Not-Expired'
```

Finally we can print the forecast.

```pycon
>>> print(ny_forecast)
Forecast for New York:
        Forecast between 2020-07-21 14:00:00 and 2020-07-21 15:00:00:
                air_pressure_at_sea_level: 1016.7hPa
                air_temperature: 28.7celsius
                cloud_area_fraction: 1.6%
                ...
```

### Accessing Data

Printing forecasts to the terminal is great but most likely you want to use the
forecast data in your own application. When the update method is run it parses
the returned data which can then be accessed through attributes of the forecast
instance.

The most notable of these is the ```data``` attribute.

```pycon
>>> type(ny_forecast.data)
<class 'metno_locationforecast.data_containers.Data'>
```

This is a special ```Data``` class which stores the weather data information.
You can list its attributes like so;

```pycon
>>> vars(ny_forecast.data).keys()
dict_keys(['last_modified', 'expires', 'updated_at', 'units', 'intervals'])
```

```last_modified```, ```expires``` and ```updated_at``` are
```datetime.datetime``` objects for when the data was last modified, when it is
expected to expire and when the forecast was updated, respectively.

```units``` contains a dictionary mapping variable names to the units in which
they are provided by the API.

```intervals``` is where we find the actual weather data. It is a list of
intervals. Note that the MET API usually supplies multiple intervals for each
time point in the data set, the forecast parser takes the *shortest* supplied
interval for each time point.

```pycon
>>> type(ny_forecast.data.intervals)
<class 'list'>
>>> type(ny_forecast.data.intervals[0])
<class 'metno_locationforecast.data_containers.Interval'>
>>> print(ny_forecast.data.intervals[0])
Forecast between 2020-07-21 14:00:00 and 2020-07-21 15:00:00:
        air_pressure_at_sea_level: 1016.7hPa
        air_temperature: 28.7celsius
        cloud_area_fraction: 1.6%
        relative_humidity: 56.0%
        wind_from_direction: 349.7degrees
        wind_speed: 1.4m/s
        precipitation_amount: 0.0mm
```

Each interval is an ```Interval``` instance. This interval class has a
```variables``` attribute which is a dictionary mapping variable names to
```Variable``` instances.

```pycon
>>> first_interval = ny_forecast.data.intervals[0]
>>> first_interval.start_time
datetime.datetime(2020, 7, 21, 14, 0)
>>> first_interval.end_time
datetime.datetime(2020, 7, 21, 15, 0)
>>> first_interval.duration
datetime.timedelta(0, 3600)
>>> first_interval.variables.keys()
dict_keys(['air_pressure_at_sea_level', 'air_temperature', 'cloud_area_fraction', 'relative_humidity', 'wind_from_direction', 'wind_speed', 'precipitation_amount'])
>>>
>>> rain = first_interval.variables["precipitation_amount"]
>>> print(rain)
precipitation_amount: 0.0mm
>>> rain.value
0.0
>>> rain.units
'mm'
```

For a full overview of the ```Data```, ```Interval``` and ```Variable``` classes
see the
[code](https://github.com/Rory-Sullivan/metno-locationforecast/blob/master/metno_locationforecast/data_containers.py).

Other attributes of the ```Forecast``` class that could be useful are;

- ```response```: This is the full ```requests.Response``` object received from the
  MET API (metno-locationforecast uses the
  [requests](https://requests.readthedocs.io/en/master/) library).
- ```json_string```: A string containing all data in json format. This is what is
  saved.
- ```json```: An object representation of the json_string.

The ```Forecast``` class also has additional methods that may be of use.

- ```save()```: Save data to save location.
- ```load()```: Load data from saved file.

The code for the ```Forecast``` class can be found
[here](https://github.com/Rory-Sullivan/metno-locationforecast/blob/master/metno_locationforecast/forecast.py).

### Custom URLs

By default the Forecast class will fetch data from
'https://api.met.no/weatherapi/locationforecast/2.0/' if you wish to use a
different domain you can pass a ```base_url``` parameter to the constructor
function. Note that the type for the forecast will be appended to this url when
requests are made, if this is not suitable for your application you should pass
an empty string for the type.

```pycon
>>> ny_forecast = Forecast(new_york, "metno-locationforecast/1.0", forecast_type="",  base_url="somewhere.com")
>>> ny_forecast.url
'somewhere.com'
```

### Configuration

If you wish to provide application wide configuration for your module this can
be done in either a ```metno-locationforecast.ini``` file or in a ```setup.cfg```
file in the root directory of your application. Below is an example of the
configurations that you can put in there showing their default values.

```ini
[metno-locationforecast]
user_agent = None
forecast_type = compact
save_location = ./data
base_url = https://api.met.no/weatherapi/locationforecast/2.0/
```

Note that regardless of the file, configurations need to be under a
```[metno-locationforecast]``` section and settings in a
```metno-locationforecast.ini``` file will take precedence.

### More Examples

For further usage examples see the
[examples](https://github.com/Rory-Sullivan/metno-locationforecast/tree/master/examples)
folder.

To see what can be done with this library you could also checkout [Dry
Rock](https://github.com/Rory-Sullivan/Dry-Rock). It is another project
maintained by myself that uses the ```metno-locationforecast``` library. It was
in fact the original inspiration for me to create this library.

## Notes on Licensing

While the code in this package is covered by an MIT license and is free to use
the weather data collected from the MET Weather API is covered by a separate
license and has it's own [terms of use](https://api.met.no/doc/TermsOfService).

## Dependencies

- [Requests](https://requests.readthedocs.io/en/master/)

## Useful Links

- PyPI page - <https://pypi.org/project/metno-locationforecast/>
- Github page - <https://github.com/Rory-Sullivan/metno-locationforecast>
- The Norwegian Meteorological Institute - <https://www.met.no/en>
- MET Weather API - <https://api.met.no/>
- MET Weather API Terms of Service - <https://api.met.no/doc/TermsOfService>
- Locationforecast/2.0 documentation - <https://api.met.no/weatherapi/locationforecast/2.0>
- Full list of variables and their names - <https://api.met.no/doc/locationforecast/datamodel>
- Yr Developer Portal - <https://developer.yr.no/>
- Yr Terms of Service (same as the MET API terms of service but perhaps more readable) - <https://developer.yr.no/doc/TermsOfService/>
- GeoNames - <http://www.geonames.org/>
- Requests library - <https://requests.readthedocs.io/en/master/>
