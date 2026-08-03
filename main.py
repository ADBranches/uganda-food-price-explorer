"""Command-line entry point for the complete Uganda food-price analysis."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from analysis import run_complete_analysis


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for reproducible analysis options."""
    parser = argparse.ArgumentParser(description="Run the complete Uganda Food Price Explorer analysis.")
    parser.add_argument("--raw-path", default="data/raw/uganda_food_prices_raw.csv")
    parser.add_argument("--cleaned-path", default="data/cleaned/uganda_food_prices_cleaned.csv")
    parser.add_argument("--output-directory", default="output")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--commodity")
    parser.add_argument("--market")
    parser.add_argument("--spike-threshold", type=float, default=25.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the full pipeline and return zero on success or one on failure."""
    args = build_parser().parse_args(argv)
    try:
        run_complete_analysis(
            raw_path=args.raw_path,
            cleaned_path=args.cleaned_path,
            output_directory=args.output_directory,
            start_date=args.start_date,
            end_date=args.end_date,
            commodity=args.commodity,
            market=args.market,
            spike_threshold=args.spike_threshold,
        )
    except (FileNotFoundError, KeyError, TypeError, ValueError) as error:
        print(f"Analysis failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
