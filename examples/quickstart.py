import stormstat

print("Loading sample data.")
df = stormstat.load_station_csv(
    "data/sample_data.csv",
    wind_speed_col="wind_speed",
    wind_dir_col="wind_dir",
)
print(f"  Loaded {len(df):,} hourly observations")
print(f"  Columns: {list(df.columns)}\n")

print("Monthly temperature summary (°C):")
summary = stormstat.monthly_summary(df, variable="temp_c")
print(summary.to_string())
print()

print("Heat index examples:")
import numpy as np
for t, rh in zip([28, 32, 35, 38], [50, 60, 70, 80]):
    hi = stormstat.heat_index(t, rh)
    print(f"  {t} °C, {rh}% RH. Heat Index {float(hi):.1f} °C")
print()

print("Wind statistics:")
stats = stormstat.wind_stats(df["wind_speed"], wind_dir=df["wind_dir"])
for k, v in stats.items():
    if k == "dir_pct":
        print("  Top directions:")
        for sector, pct in sorted(v.items(), key=lambda x: -x[1])[:3]:
            print(f"    {sector}: {pct:.1f}%")
    else:
        print(f"  {k}: {v}")
print()

print("Saving temperature plot.")
stormstat.plot_temperature(df, title="Boulder 2023 — Daily Temperature Range",
                           savepath="examples/temperature_range.png")

print("Saving wind rose.")
stormstat.plot_wind_rose(df["wind_speed"], df["wind_dir"],
                         title="Boulder 2023 — Wind Rose",
                         savepath="examples/wind_rose.png")

print("Plots saved.")