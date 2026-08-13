"""Views for the Uganda Food Price Explorer web application."""

from pathlib import Path

import pandas as pd
from django.conf import settings
from django.shortcuts import render

from data_loader import load_food_price_csv

CLEANED_DATA_PATH = settings.BASE_DIR / "data" / "cleaned" / "uganda_food_prices_cleaned.csv"


def build_dataset_overview(dataset_path: str | Path | None = None) -> dict[str, object]:
    """Load cleaned records and return summary values for the home page."""
    path = CLEANED_DATA_PATH if dataset_path is None else Path(dataset_path)
    frame = load_food_price_csv(path)
    parsed_dates = pd.to_datetime(frame["date"], errors="coerce")
    valid_dates = parsed_dates.dropna()
    if valid_dates.empty:
        raise ValueError("The dataset does not contain any valid dates.")
    return {
        "record_count": len(frame),
        "commodity_count": int(frame["commodity"].nunique(dropna=True)),
        "market_count": int(frame["market"].nunique(dropna=True)),
        "unit_count": int(frame["unit"].nunique(dropna=True)),
        "start_date": valid_dates.min().date(),
        "end_date": valid_dates.max().date(),
    }


def home(request):
    """Render the home page with a dynamic overview of the cleaned dataset."""
    context = {
        "page_title": "Uganda Food Price Explorer",
        "active_page": "home",
        "dataset_overview": None,
        "dataset_error": None,
    }
    try:
        context["dataset_overview"] = build_dataset_overview()
    except (FileNotFoundError, OSError, ValueError, pd.errors.ParserError) as error:
        context["dataset_error"] = f"Dataset overview is unavailable: {error}"
    return render(request, "explorer/home.html", context)


def explorer(request):
    """Render the page reserved for interactive dataset filters."""
    context = {
        "page_title": "Explorer | Uganda Food Price Explorer",
        "active_page": "explorer",
    }
    return render(request, "explorer/explorer.html", context)


def results(request):
    """Render the page reserved for dynamically generated results."""
    context = {
        "page_title": "Results | Uganda Food Price Explorer",
        "active_page": "results",
    }
    return render(request, "explorer/results.html", context)
