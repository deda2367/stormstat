# stormstat

Surface weather station data and visualization package for atmospheric science. This allows scientists to take CSV files to organized statistics and plots quickly.

## Installation

- pip install -e .

or 

- git clone https://github.com/deda2367/stormstat.git
- python -m install -e .
- cd stormstat


## Quick Start

Run this command:

- python examples/quickstart.py

This will generate:
- Monthly temperature summary
- Heat Index examples
- Wind statistics
- temperature_range.png
- wind_rose.png

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


## Data Source
Sample data is generated to act as mid-latitude surface observations based on Boulder, CO. Real station data can be downloaded from NOAA Climate Data Online. (https://www.ncdc.noaa.gov/cdo-web/)

##License
MIT -see LICENSE

## Author
Demi Davoll deda2367@colorado.edu
ATOC 4815/5815, University of Colorado-Boulder, Spring 2026