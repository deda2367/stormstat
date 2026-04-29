# stormstat

Surface weather station data and visualization package for atmospheric science.

## Installation

pip instal -e

## Quick Start

import stormstat

df = stormstat.load_station_csv("data/sample_data.csv", wind_speed_col="wind_speed", wind_dir_col="wind_dir")

summary = stormstat.monthly_summary(df, variable="temp_c")
print(summary)

stormstat.plot_wind_rose(df["wind_speed"], df["wind_dir"])

## API

**load_station_csv(filepath, ...)** — Loads a weather CSV into a clean DataFrame with a DatetimeIndex. Accepts any column names.

**monthly_summary(df, variable)** — Returns monthly mean, max, min, std, and count for any variable.

**heat_index(temp_c, relative_humidity)** — Computes NOAA heat index from temperature and humidity. Accepts scalars or arrays.

**wind_stats(wind_speed, wind_dir)** — Returns mean, max, percentiles, calm percentage, and dominant wind direction.

**plot_temperature(df, ...)** — Plots a shaded daily max/mean/min temperature band time series.

**plot_wind_rose(wind_speed, wind_dir, ...)** — Draws a 16-sector polar wind rose with speed bins.
