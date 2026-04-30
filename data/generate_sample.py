import numpy as np
import pandas as pd
import pathlib

rng = np.random.default_rng(2023)
dates = pd.date_range("2023-01-01", "2023-12-31 23:00", freq="h")
n = len(dates)
doy = dates.day_of_year.to_numpy()
hour = dates.hour.to_numpy()

temp = (10 + 14*np.cos(2*np.pi*(doy-200)/365)
           + 7*np.sin(2*np.pi*(hour-6)/24)
           + rng.normal(0, 2, n))
dewpoint = temp - rng.uniform(5, 15, n)
wind_speed = np.clip(rng.weibull(2, n) * 4.5, 0, 25)
wind_dir = rng.normal(270, 60, n) % 360
precip = np.where(rng.random(n) < 0.04, rng.exponential(2.0, n), 0.0)

for col_arr in [temp, dewpoint, wind_speed, wind_dir]:
    nan_idx = rng.choice(n, size=int(n * 0.005), replace=False)
    col_arr[nan_idx] = np.nan

df = pd.DataFrame({
    "datetime":   dates,
    "temp_c":     np.round(temp, 1),
    "dewpoint_c": np.round(dewpoint, 1),
    "wind_speed": np.round(wind_speed, 2),
    "wind_dir":   np.round(wind_dir, 1),
    "precip_mm":  np.round(precip, 2),
})

out = pathlib.Path(__file__).parent / "sample_data.csv"
df.to_csv(out, index=False)
print(f"Wrote {len(df):,} rows to {out}")