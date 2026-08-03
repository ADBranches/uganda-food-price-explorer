"""Grouped price summaries for Uganda Food Price Explorer."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

STAT_COLUMNS = ["record_count", "mean_price", "minimum_price", "maximum_price"]


def summarize_prices(frame: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    """Group prices, calculate transparent statistics, and sort mean price descending."""
    if frame.empty:
        return pd.DataFrame(columns=group_columns + STAT_COLUMNS)
    summary = (
        frame.groupby(group_columns, dropna=False)["price"]
        .agg(record_count="count", mean_price="mean", minimum_price="min", maximum_price="max")
        .reset_index()
    )
    return summary.sort_values(
        ["mean_price"] + group_columns,
        ascending=[False] + [True] * len(group_columns),
    ).reset_index(drop=True)


def summarize_by_commodity(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize commodity prices while keeping measurement units separate."""
    return summarize_prices(frame, ["commodity", "unit"])


def summarize_by_market(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize market and commodity prices while keeping units separate."""
    return summarize_prices(frame, ["market", "commodity", "unit"])


def write_summary(summary: pd.DataFrame, output_path: str | Path) -> Path:
    """Write one summary table to CSV and return its path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False)
    return path


MONTHLY_CHANGE_COLUMNS = [
    "commodity",
    "market",
    "unit",
    "month",
    "record_count",
    "monthly_average_price",
    "previous_month_average",
    "absolute_change",
    "percentage_change",
]


def calculate_monthly_price_changes(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly averages and month-over-month price changes by commodity, market, and unit."""
    if frame.empty:
        return pd.DataFrame(columns=MONTHLY_CHANGE_COLUMNS)
    working = frame.copy()
    working["date"] = pd.to_datetime(working["date"], errors="coerce")
    working["price"] = pd.to_numeric(working["price"], errors="coerce")
    working = working.dropna(subset=["date", "price", "commodity", "market", "unit"])
    working = working[working["price"] > 0].copy()
    working["month"] = working["date"].dt.to_period("M").astype(str)
    group_columns = ["commodity", "market", "unit", "month"]
    monthly = (
        working.groupby(group_columns, dropna=False)["price"]
        .agg(record_count="count", monthly_average_price="mean")
        .reset_index()
        .sort_values(["commodity", "market", "unit", "month"])
        .reset_index(drop=True)
    )
    series_columns = ["commodity", "market", "unit"]
    monthly["previous_month_average"] = monthly.groupby(series_columns)["monthly_average_price"].shift(1)
    monthly["absolute_change"] = monthly["monthly_average_price"] - monthly["previous_month_average"]
    monthly["percentage_change"] = (
        monthly["absolute_change"] / monthly["previous_month_average"] * 100.0
    )
    return monthly[MONTHLY_CHANGE_COLUMNS]


def identify_price_spikes(
    change_summary: pd.DataFrame,
    threshold_percent: float = 25.0,
) -> pd.DataFrame:
    """Return upward price changes at or above the documented percentage threshold."""
    if threshold_percent < 0:
        raise ValueError("Spike threshold must be zero or greater.")
    if change_summary.empty:
        return change_summary.copy()
    spikes = change_summary[
        change_summary["percentage_change"].notna()
        & (change_summary["percentage_change"] >= threshold_percent)
    ].copy()
    return spikes.sort_values(
        ["percentage_change", "commodity", "market", "unit", "month"],
        ascending=[False, True, True, True, True],
    ).reset_index(drop=True)
