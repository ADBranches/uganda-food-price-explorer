"""Reusable, non-mutating filters for Uganda Food Price Explorer."""

from __future__ import annotations

import pandas as pd


def filter_by_date_range(
    frame: pd.DataFrame,
    start_date: str | pd.Timestamp | None = None,
    end_date: str | pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Return rows within an inclusive date range without modifying the input frame."""
    result = frame.copy()
    dates = pd.to_datetime(result["date"], errors="coerce")
    start = pd.to_datetime(start_date) if start_date is not None else None
    end = pd.to_datetime(end_date) if end_date is not None else None
    if start is not None and end is not None and start > end:
        raise ValueError("Start date must be on or before end date.")
    mask = dates.notna()
    if start is not None:
        mask &= dates >= start
    if end is not None:
        mask &= dates <= end
    return result.loc[mask].copy()


def filter_by_commodity(frame: pd.DataFrame, commodity: str | None = None) -> pd.DataFrame:
    """Return exact case-insensitive commodity matches without modifying the input frame."""
    result = frame.copy()
    if commodity is None or not commodity.strip():
        return result
    target = commodity.strip().casefold()
    mask = result["commodity"].astype(str).str.strip().str.casefold() == target
    return result.loc[mask].copy()


def filter_by_market(frame: pd.DataFrame, market: str | None = None) -> pd.DataFrame:
    """Return exact case-insensitive market matches without modifying the input frame."""
    result = frame.copy()
    if market is None or not market.strip():
        return result
    target = market.strip().casefold()
    mask = result["market"].astype(str).str.strip().str.casefold() == target
    return result.loc[mask].copy()


def apply_filters(
    frame: pd.DataFrame,
    start_date: str | pd.Timestamp | None = None,
    end_date: str | pd.Timestamp | None = None,
    commodity: str | None = None,
    market: str | None = None,
) -> pd.DataFrame:
    """Apply date, commodity, and market filters and return an empty frame when no rows match."""
    result = filter_by_date_range(frame, start_date, end_date)
    result = filter_by_commodity(result, commodity)
    result = filter_by_market(result, market)
    return result.reset_index(drop=True)
