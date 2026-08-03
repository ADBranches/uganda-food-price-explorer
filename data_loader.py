"""CSV loading and raw-data profiling utilities for Uganda Food Price Explorer."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = {"date", "market", "commodity", "unit", "price"}


def load_food_price_csv(csv_path: str | Path) -> pd.DataFrame:
    """Load the food-price CSV and raise readable errors for common file problems."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    if not path.is_file():
        raise ValueError(f"CSV path is not a file: {path}")
    try:
        frame = pd.read_csv(path)
    except UnicodeDecodeError as error:
        raise ValueError(f"CSV file is not valid UTF-8 text: {path}") from error
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"CSV file is empty: {path}") from error
    if frame.empty:
        raise ValueError(f"CSV file contains no data rows: {path}")
    missing = sorted(REQUIRED_COLUMNS.difference(frame.columns))
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"CSV file is missing required columns: {joined}")
    return frame


def count_invalid_prices(frame: pd.DataFrame, price_column: str = "price") -> int:
    """Count rows where the reported price cannot be converted to a positive number."""
    numeric_prices = pd.to_numeric(frame[price_column], errors="coerce")
    invalid_mask = numeric_prices.isna() | (numeric_prices <= 0)
    return int(invalid_mask.sum())


def find_mixed_unit_commodities(frame: pd.DataFrame) -> pd.Series:
    """Return commodities that appear with more than one measurement unit."""
    units_by_commodity = frame.groupby("commodity")["unit"].nunique().sort_values(ascending=False)
    return units_by_commodity[units_by_commodity > 1]


def build_profile_lines(frame: pd.DataFrame) -> list[str]:
    """Build a text profile describing schema, completeness, duplicates, and value ranges."""
    parsed_dates = pd.to_datetime(frame["date"], errors="coerce")
    profile_lines = [
        "Uganda Food Price Raw Dataset Profile",
        "=====================================",
        "",
        f"Row count: {len(frame)}",
        f"Column count: {len(frame.columns)}",
        "",
        "Columns:",
    ]
    profile_lines.extend(f"- {column}" for column in frame.columns)
    profile_lines.extend(["", "Data types:"])
    profile_lines.extend(f"- {column}: {dtype}" for column, dtype in frame.dtypes.items())
    profile_lines.extend(["", "Missing values:"])
    profile_lines.extend(f"- {column}: {int(frame[column].isna().sum())}" for column in frame.columns)
    profile_lines.extend(
        [
            "",
            f"Duplicate rows: {int(frame.duplicated().sum())}",
            f"Invalid or non-positive prices: {count_invalid_prices(frame)}",
            f"Date parsing failures: {int(parsed_dates.isna().sum())}",
        ]
    )
    if parsed_dates.notna().any():
        profile_lines.extend(
            [
                f"Earliest date: {parsed_dates.min().date()}",
                f"Latest date: {parsed_dates.max().date()}",
            ]
        )
    profile_lines.extend(
        [
            "",
            f"Unique commodities: {frame['commodity'].nunique(dropna=True)}",
            f"Unique markets: {frame['market'].nunique(dropna=True)}",
            f"Unique units: {frame['unit'].nunique(dropna=True)}",
            "",
            "Units observed:",
        ]
    )
    unit_counts = frame["unit"].fillna("Missing").value_counts().sort_index()
    profile_lines.extend(f"- {unit}: {count}" for unit, count in unit_counts.items())
    mixed_units = find_mixed_unit_commodities(frame)
    profile_lines.extend(["", "Commodities with mixed units:"])
    if mixed_units.empty:
        profile_lines.append("- None observed")
    else:
        profile_lines.extend(f"- {commodity}: {count} units" for commodity, count in mixed_units.items())
    profile_lines.extend(["", "Top commodities by record count:"])
    commodity_counts = frame["commodity"].fillna("Missing").value_counts().head(10)
    profile_lines.extend(f"- {commodity}: {count}" for commodity, count in commodity_counts.items())
    profile_lines.extend(["", "Top markets by record count:"])
    market_counts = frame["market"].fillna("Missing").value_counts().head(10)
    profile_lines.extend(f"- {market}: {count}" for market, count in market_counts.items())
    return profile_lines


def write_profile_report(frame: pd.DataFrame, output_path: str | Path) -> Path:
    """Write the raw-data profile report and return the report path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(build_profile_lines(frame)) + "\n", encoding="utf-8")
    return path


def profile_raw_dataset(
    csv_path: str | Path = "data/raw/uganda_food_prices_raw.csv",
    output_path: str | Path = "output/raw_data_profile.txt",
) -> Path:
    """Load the raw CSV and write a profiling report for later cleaning decisions."""
    frame = load_food_price_csv(csv_path)
    return write_profile_report(frame, output_path)


if __name__ == "__main__":
    report_path = profile_raw_dataset()
    print(f"Raw data profile written to {report_path}")
