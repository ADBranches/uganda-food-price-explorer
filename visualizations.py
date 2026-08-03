"""Readable charts for Uganda Food Price Explorer findings."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def create_highest_average_prices_chart(
    commodity_summary: pd.DataFrame,
    output_path: str | Path,
    unit: str = "KG",
    top_n: int = 10,
) -> Path:
    """Create a sorted bar chart for the highest average prices within one unit."""
    selected = commodity_summary[commodity_summary["unit"].eq(unit)].copy()
    selected = selected.sort_values("mean_price", ascending=False).head(top_n)
    if selected.empty:
        raise ValueError(f"No commodity summary rows found for unit: {unit}")
    selected = selected.sort_values("mean_price", ascending=True)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(11, 7))
    bars = axis.barh(selected["commodity"], selected["mean_price"])
    axis.set_title(f"Highest Average Food Prices in Uganda ({unit})")
    axis.set_xlabel(f"Average price in UGX per {unit}")
    axis.set_ylabel("Commodity")
    axis.grid(axis="x", alpha=0.3)
    labels = [f"UGX {value:,.0f}  n={count}" for value, count in zip(selected["mean_price"], selected["record_count"])]
    axis.bar_label(bars, labels=labels, padding=4, fontsize=8)
    axis.set_xlim(0, selected["mean_price"].max() * 1.35)
    figure.text(0.01, 0.01, f"Top {len(selected)} commodities ranked within a single measurement unit. n is the record count.", fontsize=8)
    figure.tight_layout(rect=(0, 0.04, 1, 1))
    figure.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return path


def create_price_trends_chart(
    change_summary: pd.DataFrame,
    output_path: str | Path,
    commodity: str = "Beans",
    unit: str = "KG",
    top_markets: int = 5,
) -> Path:
    """Create a monthly trend chart for one commodity and unit across selected markets."""
    selected = change_summary[
        change_summary["commodity"].eq(commodity) & change_summary["unit"].eq(unit)
    ].copy()
    if selected.empty:
        raise ValueError(f"No monthly trend rows found for {commodity} measured in {unit}")
    market_counts = selected.groupby("market")["record_count"].sum().nlargest(top_markets)
    selected = selected[selected["market"].isin(market_counts.index)].copy()
    selected["month_date"] = pd.to_datetime(selected["month"], format="%Y-%m", errors="coerce")
    selected = selected.dropna(subset=["month_date", "monthly_average_price"])
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(12, 7))
    for market, group in selected.groupby("market"):
        group = group.sort_values("month_date")
        axis.plot(group["month_date"], group["monthly_average_price"], marker="o", markersize=2.5, linewidth=1.4, label=f"{market} (n={int(group['record_count'].sum())})")
    axis.set_title(f"Monthly Average Price Trends for {commodity} ({unit})")
    axis.set_xlabel("Month")
    axis.set_ylabel(f"Average price in UGX per {unit}")
    axis.grid(alpha=0.3)
    axis.legend(title=f"Top {len(market_counts)} markets by observations", fontsize=8)
    figure.autofmt_xdate()
    figure.text(0.01, 0.01, "Each line uses one commodity and one measurement unit. Legend n is the total observation count.", fontsize=8)
    figure.tight_layout(rect=(0, 0.04, 1, 1))
    figure.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return path
