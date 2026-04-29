import argparse
import sys


def cmd_summary(args):
    from .core import load_station_csv, monthly_summary
    df = load_station_csv(args.file, wind_speed_col=args.speed_col or None,
                          wind_dir_col=args.dir_col or None)
    summary = monthly_summary(df, variable=args.variable)
    print(f"\nMonthly summary for '{args.variable}':\n")
    print(summary.to_string())
    print()


def cmd_wind(args):
    from .core import load_station_csv, wind_stats
    df = load_station_csv(args.file, wind_speed_col=args.speed,
                          wind_dir_col=args.dir or None)
    if "wind_speed" not in df.columns:
        print("Error: No wind speed column found.")
        sys.exit(1)
    stats = wind_stats(df["wind_speed"],
                       wind_dir=df["wind_dir"] if "wind_dir" in df.columns else None)
    print("\nWind statistics:\n")
    for k, v in stats.items():
        if k == "dir_pct":
            print("  dir_pct:")
            for sector, pct in v.items():
                print(f"    {sector:3s}: {pct:.1f}%")
        else:
            print(f"  {k}: {v}")
    print()


def cmd_plot(args):
    from .core import load_station_csv
    from .viz import plot_temperature
    df = load_station_csv(args.file, temp_col=args.temp_col)
    fig = plot_temperature(df, temp_col=args.temp_col,
                           title=args.title, savepath=args.output)
    if args.output is None:
        import matplotlib.pyplot as plt
        plt.show()


def main():
    parser = argparse.ArgumentParser(prog="stormstat",
                                     description="Surface weather station statistics toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_summary = subparsers.add_parser("summary", help="Print monthly statistics")
    p_summary.add_argument("file")
    p_summary.add_argument("--variable", default="temp_c")
    p_summary.add_argument("--speed-col", default=None, dest="speed_col")
    p_summary.add_argument("--dir-col", default=None, dest="dir_col")
    p_summary.set_defaults(func=cmd_summary)

    p_wind = subparsers.add_parser("wind", help="Print wind statistics")
    p_wind.add_argument("file")
    p_wind.add_argument("--speed", required=True)
    p_wind.add_argument("--dir", default=None)
    p_wind.set_defaults(func=cmd_wind)

    p_plot = subparsers.add_parser("plot", help="Plot daily temperature range")
    p_plot.add_argument("file")
    p_plot.add_argument("--temp-col", default="temp_c", dest="temp_col")
    p_plot.add_argument("--title", default=None)
    p_plot.add_argument("-o", "--output", default=None)
    p_plot.set_defaults(func=cmd_plot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()