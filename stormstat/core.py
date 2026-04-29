import numpy as np
import pandas as pd


def load_station_csv(filepath, datetime_col="datetime", temp_col="temp_c",
                     dewpoint_col=None, wind_speed_col=None,
                     wind_dir_col=None, precip_col=None):
    """
    Load a surface weather station CSV into a clean, typed DataFrame.

    Parameters:
    filepath : str or pathlib.Path
        Path to the CSV file.
    datetime_col : str, optional
        Name of the column containing date/time strings. 
    temp_col : str, optional
        Name of the temperature column (°C).
    dewpoint_col : str or None, optional
        Name of the dewpoint column (°C). 
    wind_speed_col : str or None, optional
        Name of the wind speed column (m/s). 
    wind_dir_col : str or None, optional
        Name of the wind direction column (degrees). 
    precip_col : str or None, optional
        Name of the precipitation column (mm). 
    Returns:
    pandas.DataFrame
        DataFrame with a DatetimeIndex and standardised column names:
        temp_c, dewpoint_c, wind_speed, wind_dir, precip_mm.

    Errors:
    FileNotFoundError
        If filepath does not exist.
    ValueError
        If datetime_col is not found in the CSV.
    """
    import pathlib

    path = pathlib.Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"No file found at: {filepath}")

    df = pd.read_csv(path)

    if datetime_col not in df.columns:
        raise ValueError(
            f"Column '{datetime_col}' not found in CSV. "
            f"Available columns: {list(df.columns)}"
        )

    df[datetime_col] = pd.to_datetime(df[datetime_col], errors="coerce")
    df = df.dropna(subset=[datetime_col])
    df = df.set_index(datetime_col)
    df.index.name = "datetime"

    rename = {}
    col_map = {
        temp_col: "temp_c",
        dewpoint_col: "dewpoint_c",
        wind_speed_col: "wind_speed",
        wind_dir_col: "wind_dir",
        precip_col: "precip_mm",
    }
    for src, dst in col_map.items():
        if src is not None:
            if src not in df.columns:
                raise ValueError(
                    f"Column '{src}' not found in CSV. "
                    f"Available columns: {list(df.columns)}"
                )
            rename[src] = dst

    df = df.rename(columns=rename)
    keep = [c for c in ["temp_c", "dewpoint_c", "wind_speed", "wind_dir", "precip_mm"]
            if c in df.columns]
    return df[keep].copy()


def monthly_summary(df, variable="temp_c"):
    """
    Compute monthly mean, maximum, minimum, and standard deviation.

    Parameters:
    df : pandas.DataFrame
        DataFrame with a DatetimeIndex, as returned by load_station_csv.
    variable : str, optional
        Column name to summarise. Default "temp_c".

    Returns:
    pandas.DataFrame
        DataFrame indexed by (year, month) with columns
        mean, max, min, std, and count.
    Errors:
    ValueError
        If variable is not a column in df, or if df lacks a DatetimeIndex.
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("df must have a DatetimeIndex. Use load_station_csv() first.")
    if variable not in df.columns:
        raise ValueError(
            f"Variable '{variable}' not found. Available: {list(df.columns)}"
        )

    grouped = df[variable].groupby([df.index.year, df.index.month])
    summary = grouped.agg(mean="mean", max="max", min="min", std="std", count="count")
    summary.index.names = ["year", "month"]
    return summary.round(2)


def heat_index(temp_c, relative_humidity):
    """
    Calculate the NOAA heat index from air temperature and relative humidity.

    Using the Rothfusz equation for hot/humid conditions,
    and the simpler Steadman equation for other conditions.

    Parameters:
    temp_c : float or array_like
        Air temperature in degrees Celsius.
    relative_humidity : float or array_like
        Relative humidity in percent (0-100).

    Returns:
    numpy.ndarray
        Heat index in degrees Celsius.

    Errors:
    ValueError
        If relative_humidity contains values outside 0-100.
    """
    T = np.asarray(temp_c, dtype=float)
    RH = np.asarray(relative_humidity, dtype=float)

    if np.any(RH < 0) or np.any(RH > 100):
        raise ValueError("relative_humidity values must be between 0 and 100.")

    T_f = T * 9.0 / 5.0 + 32.0

    hi_simple = 0.5 * (T_f + 61.0 + (T_f - 68.0) * 1.2 + RH * 0.094)

    C = [-42.379, 2.04901523, 10.14333127, -0.22475541,
         -0.00683783, -0.05481717, 0.00122874, 0.00085282, -0.00000199]

    hi_full = (C[0] + C[1]*T_f + C[2]*RH + C[3]*T_f*RH
               + C[4]*T_f**2 + C[5]*RH**2 + C[6]*T_f**2*RH
               + C[7]*T_f*RH**2 + C[8]*T_f**2*RH**2)

    use_full = (hi_simple >= 160) & (T_f >= 80) & (RH >= 40)
    hi_f = np.where(use_full, hi_full, hi_simple)
    hi_c = (hi_f - 32.0) * 5.0 / 9.0
    return np.round(hi_c, 1)


def wind_stats(wind_speed, wind_dir=None, percentiles=(50, 90, 95)):
    """
    Compute summary statistics for wind speed and optionally wind direction.

    Parameters
    ----------
    wind_speed : array_like
        Wind speed values (m/s).
    wind_dir : array_like or None, optional
        Wind direction in degrees (0-360).
    percentiles : tuple of int, optional
        Percentiles to compute.

    Returns
    -------
    dict
        Keys: mean, max, std, calm_pct, p{N} for each percentile,
        and (if wind_dir given) dominant_dir, dir_pct.

    Errors
    ------
    ValueError
        If wind_speed contains only NaN, or any negative values.
    """
    spd = np.asarray(wind_speed, dtype=float)
    spd_valid = spd[~np.isnan(spd)]

    if len(spd_valid) == 0:
        raise ValueError("wind_speed contains no valid (non-NaN) values.")
    if np.any(spd_valid < 0):
        raise ValueError("wind_speed contains negative values.")

    stats = {
        "mean": round(float(np.mean(spd_valid)), 2),
        "max": round(float(np.max(spd_valid)), 2),
        "std": round(float(np.std(spd_valid)), 2),
        "calm_pct": round(float(np.mean(spd_valid < 0.5) * 100), 2),
    }
    for p in percentiles:
        stats[f"p{p}"] = round(float(np.percentile(spd_valid, p)), 2)

    if wind_dir is not None:
        dirs = np.asarray(wind_dir, dtype=float)
        dirs = dirs[~np.isnan(dirs)] % 360

        sectors = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        edges = np.arange(22.5, 360, 45)
        indices = np.digitize(dirs, edges)
        sector_counts = np.bincount(indices % 8, minlength=8)
        sector_pct = {s: round(float(c / len(dirs) * 100), 1)
                      for s, c in zip(sectors, sector_counts)}

        stats["dominant_dir"] = sectors[int(np.argmax(sector_counts))]
        stats["dir_pct"] = sector_pct

    return stats