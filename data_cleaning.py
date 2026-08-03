"""Reproducible data cleaning for Uganda Food Price Explorer."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_loader import load_food_price_csv

TEXT_COLUMNS = ["admin1", "admin2", "market", "category", "commodity", "unit", "priceflag", "pricetype", "currency"]
REQUIRED_COLUMNS = ["date", "market", "commodity", "unit", "price"]


def normalize_text_value(value: object) -> str:
    """Return a trimmed text value with repeated whitespace collapsed."""
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().split())


def normalize_text_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with known text columns normalized for consistent grouping."""
    cleaned = frame.copy()
    for column in TEXT_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].map(normalize_text_value)
    return cleaned


def convert_dates(frame: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    """Return a copy with the date column converted to pandas datetime values."""
    cleaned = frame.copy()
    cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")
    return cleaned


def convert_prices(frame: pd.DataFrame, column: str = "price") -> pd.DataFrame:
    """Return a copy with the price column converted to numeric values."""
    cleaned = frame.copy()
    cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    return cleaned


def remove_unusable_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove rows that cannot support date, market, commodity, unit, and price analysis."""
    cleaned = frame.copy()
    text_ready = cleaned[["market", "commodity", "unit"]].ne("").all(axis=1)
    date_ready = cleaned["date"].notna()
    price_ready = cleaned["price"].notna() & (cleaned["price"] > 0)
    return cleaned[text_ready & date_ready & price_ready].copy()


def clean_food_price_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Clean raw food-price rows into a deterministic analysis-ready DataFrame."""
    cleaned = normalize_text_columns(frame)
    cleaned = convert_dates(cleaned)
    cleaned = convert_prices(cleaned)
    cleaned = cleaned.drop_duplicates().copy()
    cleaned = remove_unusable_rows(cleaned)
    cleaned = cleaned.sort_values(["date", "market", "commodity", "unit", "price"]).reset_index(drop=True)
    return cleaned


def write_cleaned_data(frame: pd.DataFrame, output_path: str | Path) -> Path:
    """Write a cleaned DataFrame to CSV with dates stored as YYYY-MM-DD strings."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    output = frame.copy()
    output["date"] = output["date"].dt.strftime("%Y-%m-%d")
    output.to_csv(path, index=False)
    return path


def clean_raw_dataset(
    csv_path: str | Path = "data/raw/uganda_food_prices_raw.csv",
    output_path: str | Path = "data/cleaned/uganda_food_prices_cleaned.csv",
) -> Path:
    """Load the raw dataset, clean it reproducibly, and write the cleaned CSV."""
    raw_frame = load_food_price_csv(csv_path)
    cleaned_frame = clean_food_price_data(raw_frame)
    return write_cleaned_data(cleaned_frame, output_path)


if __name__ == "__main__":
    cleaned_path = clean_raw_dataset()
    print(f"Cleaned data written to {cleaned_path}")
