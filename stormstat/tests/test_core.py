import numpy as np
import pandas as pd
import pytest

from stormstat.core import heat_index, wind_stats, monthly_summary


class TestHeatIndex:
    def test_scalar_known_value(self):
        result = heat_index(35.0, 60.0)
        assert abs(float(result) - 36.1) < 1.0

    def test_array_input(self):
        result = heat_index([30, 35], [50, 70])
        assert result.shape == (2,)

    def test_cool_conditions(self):
        result = heat_index(20.0, 50.0)
        assert float(result) < 30.0

    def test_invalid_humidity_raises(self):
        with pytest.raises(ValueError, match="between 0 and 100"):
            heat_index(30.0, 110.0)

    def test_zero_humidity(self):
        result = heat_index(30.0, 0.0)
        assert np.isfinite(result).all()


class TestWindStats:
    def setup_method(self):
        rng = np.random.default_rng(42)
        self.speed = rng.uniform(0, 10, 500)
        self.dirs = rng.uniform(0, 360, 500)

    def test_returns_expected_keys(self):
        stats = wind_stats(self.speed)
        for key in ("mean", "max", "std", "calm_pct", "p50", "p90", "p95"):
            assert key in stats

    def test_with_direction(self):
        stats = wind_stats(self.speed, self.dirs)
        assert "dominant_dir" in stats
        assert "dir_pct" in stats
        assert sum(stats["dir_pct"].values()) == pytest.approx(100.0, abs=1.0)

    def test_nan_ignored(self):
        spd = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
        stats = wind_stats(spd)
        assert stats["mean"] == pytest.approx(3.0, abs=0.1)

    def test_all_nan_raises(self):
        with pytest.raises(ValueError, match="no valid"):
            wind_stats(np.array([np.nan, np.nan]))

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="negative"):
            wind_stats(np.array([1.0, -2.0, 3.0]))

    def test_calm_percentage(self):
        spd = np.array([0.0, 0.0, 5.0, 5.0])
        stats = wind_stats(spd)
        assert stats["calm_pct"] == pytest.approx(50.0)


class TestMonthlySummary:
    def setup_method(self):
        dates = pd.date_range("2025-01-01", "2025-12-31", freq="h")
        rng = np.random.default_rng(7)
        self.df = pd.DataFrame({"temp_c": rng.normal(15, 8, len(dates))}, index=dates)

    def test_returns_12_months(self):
        assert len(monthly_summary(self.df)) == 12

    def test_columns_present(self):
        summary = monthly_summary(self.df)
        for col in ("mean", "max", "min", "std", "count"):
            assert col in summary.columns

    def test_max_geq_mean_geq_min(self):
        summary = monthly_summary(self.df)
        assert (summary["max"] >= summary["mean"]).all()
        assert (summary["mean"] >= summary["min"]).all()

    def test_missing_variable_raises(self):
        with pytest.raises(ValueError, match="not found"):
            monthly_summary(self.df, variable="wind_speed")

    def test_non_datetime_index_raises(self):
        with pytest.raises(ValueError, match="DatetimeIndex"):
            monthly_summary(self.df.reset_index(drop=True))