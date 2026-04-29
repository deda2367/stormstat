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

# load_station_csv()
Loads a weather CSV into a DataFrame with a DatetimeIndex.

# monthly_summary()
 Returns monthly mean, max, min, std, and count.

# heat_index()
Computes NOAA heat index from temperature and humidity. Accepts scalars or arrays.

# wind_stats()
Returns mean, max, percentiles, calm and dominant wind direction.

# plot_temperature()
Creates a daily max/mean/min temperature band time series.

# plot_wind_rose()
Creates a wind rose band chart.
