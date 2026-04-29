import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_temperature(df, temp_col="temp_c", title=None, figsize=(12, 4),
                     color_max="red", color_min="blue", savepath=None):
    """
    Plot a daily temperature range time series (max/mean/min).

    Parameters:
    df : pandas.DataFrame
        DataFrame with a DatetimeIndex and a temperature column.
    temp_col : str, optional
        Name of the temperature column. 
    title : str or None, optional
        Plot title.
    figsize : tuple, optional
        Figure size in inches. 
    color_max : str, optional
        Colour for the warm side of the band. 
    color_min : str, optional
        Colour for the cool side of the band. 
    savepath : str or None, optional
        Save figure.

    Returns:
    matplotlib.figure.Figure

    Errors:
    ValueError
        If temp_col is not in df.
    """
    if temp_col not in df.columns:
        raise ValueError(f"Column '{temp_col}' not found. Available: {list(df.columns)}")

    daily = df[temp_col].resample("D").agg(["max", "mean", "min"]).dropna()

    fig, ax = plt.subplots(figsize=figsize)
    ax.fill_between(daily.index, daily["max"], daily["min"],
                    alpha=0.25, color="purple", label="Daily range")
    ax.plot(daily.index, daily["mean"], color="green", lw=1.5, label="Daily mean")
    ax.plot(daily.index, daily["max"], color=color_max, lw=0.8, alpha=0.6, label="Daily max")
    ax.plot(daily.index, daily["min"], color=color_min, lw=0.8, alpha=0.6, label="Daily min")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
    ax.set_ylabel("Temperature (°C)", fontsize=11)
    ax.set_title(title or f"Daily Temperature Range — {temp_col}", fontsize=13)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()

    if savepath:
        fig.savefig(savepath, dpi=150, bbox_inches="tight")
        print(f"Figure saved to {savepath}")
    return fig


def plot_wind_rose(wind_speed, wind_dir, bins=None, title="Wind Rose",
                   figsize=(6, 6), cmap="YlOrRd", savepath=None):
    """
    Draw a wind rose from speed and direction arrays.

    Parameters:
    wind_speed : array_like
        Wind speed values (m/s).
    wind_dir : array_like
        Wind direction in degrees (0 = North, clockwise).
    bins : list of float or None, optional
        Speed bin edges in m/s. 
    title : str, optional
        Plot title. Default "Wind Rose".
    figsize : tuple, optional
        Figure size. Default (6, 6).
    cmap : str, optional
        Matplotlib colormap.
    savepath : str or None, optional
        Save Figure.

    Returns:
    matplotlib.figure.Figure

   Errors:
    ValueError
        If wind_speed and wind_dir have different lengths.
    """
    spd = np.asarray(wind_speed, dtype=float)
    dirs = np.asarray(wind_dir, dtype=float)

    if spd.shape != dirs.shape:
        raise ValueError("wind_speed and wind_dir must have the same shape.")

    mask = ~(np.isnan(spd) | np.isnan(dirs))
    spd, dirs = spd[mask], dirs[mask]

    if len(spd) == 0:
        raise ValueError("No valid observations.")

    if bins is None:
        bins = [0, 2, 4, 6, 9, 100]
    bin_labels = [f"{bins[i]}–{bins[i+1]} m/s" for i in range(len(bins) - 1)]
    bin_labels[-1] = f">{bins[-2]} m/s"

    n_sectors = 16
    sector_width = 360 / n_sectors
    sector_angles = np.deg2rad(np.arange(0, 360, sector_width))

    dirs_norm = dirs % 360
    sector_indices = (dirs_norm / sector_width).astype(int) % n_sectors
    speed_bin_indices = np.clip(np.digitize(spd, bins) - 1, 0, len(bins) - 2)

    freq = np.zeros((n_sectors, len(bins) - 1))
    for s_idx, b_idx in zip(sector_indices, speed_bin_indices):
        freq[s_idx, b_idx] += 1
    freq = freq / len(spd) * 100

    colors = plt.get_cmap(cmap)(np.linspace(0.2, 0.95, len(bins) - 1))
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    bar_width = np.deg2rad(sector_width) * 0.9
    bottom = np.zeros(n_sectors)

    for b in range(len(bins) - 1):
        ax.bar(sector_angles, freq[:, b], width=bar_width,
               bottom=bottom, color=colors[b], label=bin_labels[b],
               edgecolor="white", linewidth=0.4, alpha=0.9)
        bottom += freq[:, b]

    ax.set_xticks(np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]))
    ax.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], fontsize=10)
    ax.set_title(title, fontsize=13, pad=18)

    max_r = np.ceil(bottom.max() / 5) * 5
    ax.set_ylim(0, max_r)
    ax.set_yticks(np.linspace(0, max_r, 4)[1:])
    ax.set_yticklabels([f"{v:.0f}%" for v in np.linspace(0, max_r, 4)[1:]], fontsize=7)
    ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.0),
              fontsize=8, title="Speed", title_fontsize=9)

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=150, bbox_inches="tight")
        print(f"Figure saved to {savepath}")
    return fig