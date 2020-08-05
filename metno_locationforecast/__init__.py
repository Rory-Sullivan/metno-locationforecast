"""A Python interface for the MET Norway Locationforecast/2.0 service.

Classes:
    Place: Holds data for a place
    Forecast: Retrieves, stores and updates forecast data

Modules:
    forecast: Holds the Forecast class
    data_containers: Holds classes for storing data
"""

from .forecast import Forecast
from .data_containers import Place

__all__ = ["Place", "Forecast", "forecast", "data_containers"]
