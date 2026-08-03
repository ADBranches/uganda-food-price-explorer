"""Analysis workflows for Uganda Food Price Explorer."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_cleaning import clean_food_price_data, write_cleaned_data
from data_loader import load_food_price_csv, write_profile_report
from filters import apply_filters
from summaries import calculate_monthly_price_changes, identify_price_spikes, summarize_by_commodity, summarize_by_market, write_summary
from visualizations import create_highest_average_prices_chart, create_price_trends_chart


def answer_question_one(frame: pd.DataFrame, output_directory: str | Path = "output", start_date: str | None = None, end_date: str | None = None, commodity: str | None = None, market: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Filter records, export grouped summaries, and return Question 1 results."""
    filtered = apply_filters(frame, start_date=start_date, end_date=end_date, commodity=commodity, market=market)
    commodity_summary = summarize_by_commodity(filtered)
    market_summary = summarize_by_market(filtered)
    output_dir = Path(output_directory)
    write_summary(commodity_summary, output_dir / "summary_by_commodity.csv")
    write_summary(market_summary, output_dir / "summary_by_market.csv")
    return commodity_summary, market_summary


def run_question_one(cleaned_path: str | Path = "data/cleaned/uganda_food_prices_cleaned.csv", output_directory: str | Path = "output") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load cleaned records and generate both Question 1 output tables."""
    return answer_question_one(pd.read_csv(cleaned_path), output_directory)


def answer_question_two(frame: pd.DataFrame, output_directory: str | Path = "output", threshold_percent: float = 25.0, start_date: str | None = None, end_date: str | None = None, commodity: str | None = None, market: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate monthly price changes, detect spikes, and export Question 2 tables."""
    filtered = apply_filters(frame, start_date=start_date, end_date=end_date, commodity=commodity, market=market)
    change_summary = calculate_monthly_price_changes(filtered)
    spikes = identify_price_spikes(change_summary, threshold_percent)
    output_dir = Path(output_directory)
    write_summary(change_summary, output_dir / "price_change_summary.csv")
    write_summary(spikes, output_dir / "price_spikes.csv")
    return change_summary, spikes


def run_question_two(cleaned_path: str | Path = "data/cleaned/uganda_food_prices_cleaned.csv", output_directory: str | Path = "output", threshold_percent: float = 25.0) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load cleaned records and generate both Question 2 output tables."""
    return answer_question_two(pd.read_csv(cleaned_path), output_directory=output_directory, threshold_percent=threshold_percent)


def create_analysis_charts(commodity_summary: pd.DataFrame, change_summary: pd.DataFrame, output_directory: str | Path = "output/charts") -> tuple[Path, Path]:
    """Create the Question 1 bar chart and Question 2 monthly trend chart."""
    output_dir = Path(output_directory)
    bar_path = create_highest_average_prices_chart(commodity_summary, output_dir / "highest_average_prices.png", unit="KG", top_n=10)
    trend_path = create_price_trends_chart(change_summary, output_dir / "price_trends.png", commodity="Beans", unit="KG", top_markets=5)
    return bar_path, trend_path




def run_complete_analysis(
    raw_path: str | Path = "data/raw/uganda_food_prices_raw.csv",
    cleaned_path: str | Path = "data/cleaned/uganda_food_prices_cleaned.csv",
    output_directory: str | Path = "output",
    start_date: str | None = None,
    end_date: str | None = None,
    commodity: str | None = None,
    market: str | None = None,
    spike_threshold: float = 25.0,
) -> dict[str, object]:
    """Run loading, profiling, cleaning, filtering, summaries, exports, and charts."""
    if spike_threshold < 0:
        raise ValueError("Spike threshold must be zero or greater.")
    raw_path = Path(raw_path)
    cleaned_path = Path(cleaned_path)
    output_dir = Path(output_directory)
    raw_frame = load_food_price_csv(raw_path)
    profile_path = write_profile_report(raw_frame, output_dir / "raw_data_profile.txt")
    cleaned_frame = clean_food_price_data(raw_frame)
    write_cleaned_data(cleaned_frame, cleaned_path)
    filtered_frame = apply_filters(cleaned_frame, start_date=start_date, end_date=end_date, commodity=commodity, market=market)
    if filtered_frame.empty:
        raise ValueError("Active filters returned no rows.")
    commodity_summary = summarize_by_commodity(filtered_frame)
    market_summary = summarize_by_market(filtered_frame)
    change_summary = calculate_monthly_price_changes(filtered_frame)
    spikes = identify_price_spikes(change_summary, spike_threshold)
    commodity_path = write_summary(commodity_summary, output_dir / "summary_by_commodity.csv")
    market_path = write_summary(market_summary, output_dir / "summary_by_market.csv")
    change_path = write_summary(change_summary, output_dir / "price_change_summary.csv")
    spike_path = write_summary(spikes, output_dir / "price_spikes.csv")
    kg_summary = commodity_summary[commodity_summary["unit"].eq("KG")]
    if kg_summary.empty:
        raise ValueError("The filtered data contains no KG rows for chart generation.")
    chart_commodity = commodity if commodity is not None else "Beans"
    trend_rows = change_summary[change_summary["commodity"].eq(chart_commodity) & change_summary["unit"].eq("KG")]
    if trend_rows.empty:
        kg_changes = change_summary[change_summary["unit"].eq("KG")]
        if kg_changes.empty:
            raise ValueError("The filtered data contains no KG monthly trends.")
        chart_commodity = str(kg_changes.groupby("commodity")["record_count"].sum().idxmax())
    bar_path = create_highest_average_prices_chart(commodity_summary, output_dir / "charts/highest_average_prices.png", unit="KG", top_n=10)
    trend_path = create_price_trends_chart(change_summary, output_dir / "charts/price_trends.png", commodity=chart_commodity, unit="KG", top_markets=5)
    filters = {"start_date": start_date, "end_date": end_date, "commodity": commodity, "market": market, "spike_threshold": spike_threshold}
    outputs = [profile_path, cleaned_path, commodity_path, market_path, change_path, spike_path, bar_path, trend_path]
    highest_kg_commodity = str(kg_summary.iloc[0]["commodity"])
    active_filters = ", ".join(f"{key}={value}" for key, value in filters.items() if value is not None)
    print(f"Source: {raw_path}")
    print(f"Raw rows: {len(raw_frame)}")
    print(f"Cleaned rows: {len(cleaned_frame)}")
    print(f"Filtered rows: {len(filtered_frame)}")
    print(f"Active filters: {active_filters}")
    print(f"Highest average KG commodity: {highest_kg_commodity}")
    print(f"Detected price spikes: {len(spikes)}")
    print("Outputs:")
    for path in outputs:
        print(f"  {path}")
    return {"raw_rows": len(raw_frame), "cleaned_rows": len(cleaned_frame), "filtered_rows": len(filtered_frame), "filters": filters, "outputs": outputs}
