# Changelog

All notable changes to this project will be documented in this file. Changes
coming in future releases can be found in the [unreleased](#[Unreleased])
section.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2024-07-02

A minor release adding some functionality.

### Added

- Adds ability to convert wind speeds to Beaufort scale

## [1.1.0] - 2022-01-01

A minor release adding some functionality.

### Added

- Save location configuration now has support for home directory ('~/') and
  relative ('../') path notations, fixing
  [#3](https://github.com/Rory-Sullivan/metno-locationforecast/issues/3)
- Updates requests dependency to be more permissive, fixing
  [#5](https://github.com/Rory-Sullivan/metno-locationforecast/issues/5)

## [1.0.0] - 2020-08-21

The first official release.

### Added

- Place class for storing location information
- Forecast class for handling fetching, parsing, storing and caching of data
  - Update method for performing an all-encompassing update of data
  - Load method for loading data from a cached file
  - Save method for saving data
- Data class for storing data
- Interval class for storing data related to an interval
  - Methods for retrieving intervals for a given day and intervals between given
    times
- Variable class for storing variables
  - Support equality and comparison operations provided units are the same
  - Method for converting units
- Support for configuration to be stored in a configuration file (setup.cfg or
  .locationforecast)
