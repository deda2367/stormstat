"""
stormstat — Surface weather station statistics and visualization toolkit.

Public API
----------
load_station_csv   : Load a CSV of weather observations into a clean DataFrame
monthly_summary    : Compute monthly mean/max/min/std for any variable
heat_index         : Calculate the NOAA heat index from temperature and humidity
wind_stats         : Compute wind speed statistics and return a summary dict
plot_temperature   : Plot a daily temperature range time series
plot_wind_rose     : Draw a wind rose from speed and direction arrays
"""

from .core import (
    load_station_csv,
    monthly_summary,
    heat_index,
    wind_stats,
)
from .viz import plot_temperature, plot_wind_rose

__all__ = [
    "load_station_csv",
    "monthly_summary",
    "heat_index",
    "wind_stats",
    "plot_temperature",
    "plot_wind_rose",
]

__version__ = "0.1.0"