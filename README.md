# Uganda Food Price Explorer

## Overview

Uganda Food Price Explorer is a reproducible Python data-analysis project created for CSE 310 Module 2. It studies historical food-price observations from Ugandan markets with Pandas and Matplotlib. The complete workflow loads, profiles, cleans, filters, summarizes, exports, tests, and visualizes the data.

## Analysis Questions

1. Which commodities and markets have the highest average reported prices, and how do the results change when a date, commodity, or market filter is applied?
2. Which commodities show the largest price increases over time, and during which months do unusual upward price changes appear?

## Dataset

- **Title:** Uganda - Food Prices
- **Publisher:** World Food Programme
- **Platform:** Humanitarian Data Exchange
- **Dataset page:** https://data.humdata.org/dataset/wfp-food-prices-for-uganda
- **License:** Creative Commons Attribution for Intergovernmental Organisations, CC BY-IGO
- **Accessed:** August 2, 2026
- **Raw records:** 32,115
- **Date range:** January 2006 through June 2026
- **Coverage:** 38 commodities, 43 markets, and 5 measurement units

The raw CSV is preserved at `data/raw/uganda_food_prices_raw.csv`. Its SHA-256 checksum is stored at `data/raw/uganda_food_prices_raw.csv.sha256`.

## Data Preparation

The cleaning workflow normalizes text labels, converts dates and prices, removes exact duplicates, rejects unusable or non-positive records, and writes the analysis-ready CSV to `data/cleaned/uganda_food_prices_cleaned.csv`.

The final audit found no required-field nulls, duplicate rows, invalid dates, non-finite prices, non-positive prices, or blank analytical labels.

## Filters

The command-line workflow supports inclusive start and end dates, case-insensitive commodity and market matching, combined filters, and validation for reversed date ranges and empty results. Run `python3 main.py --help` to view every option.

## Analysis Methods

### Question 1

Commodity summaries group by `commodity` and `unit`. Market summaries group by `market`, `commodity`, and `unit`. Each group contains record count, mean price, minimum price, and maximum price. Results are sorted by mean price in descending order. Unit remains part of every grouping key so incompatible measurements are not treated as equivalent.

### Question 2

Dates are converted to monthly periods. Records are grouped by commodity, market, unit, and month. The workflow calculates monthly record count, monthly average price, previous observed monthly average, absolute change, and percentage change.

An upward price spike is a month-over-month increase of **at least 25 percent**. The boundary is inclusive, so 25.0 percent qualifies while 24.99 percent does not.

## Verified Findings

- Cleaned rows: 32,115
- Highest average KG commodity: Dried fish, approximately UGX 20,358 per KG from 725 records
- Commodity summary rows: 38
- Market summary rows: 638
- Monthly price-change rows: 31,320
- Spike rows meeting the inclusive 25 percent rule: 2,759
- Automated tests: 36 passing

## Charts

- `output/charts/highest_average_prices.png` shows the ten highest average KG prices with average values and record counts.
- `output/charts/price_trends.png` shows monthly Beans-per-KG trends for the five markets with the most observations, with sample sizes in the legend.

## Limitations

Monthly observations are sparse. Every exported commodity-market-unit-month group contains fewer than three source observations, so month-over-month changes and spike classifications may be sensitive to individual observations. One market summary contains only two records.

Record counts remain in exported tables and chart labels or legends. The 25 percent threshold is a reproducible classification rule, not proof of an economic shock or its cause.

## Environment and Installation

Verified with Python 3.13.12.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

## Run the Complete Analysis

```bash
.venv/bin/python main.py
```

Example with filters:

```bash
.venv/bin/python main.py --start-date 2024-01-01 --end-date 2024-12-31 --commodity Beans --market Owino
```

## Run the Tests

```bash
.venv/bin/python -m unittest tests/test_analysis.py -v
```

Expected result:

```text
Ran 36 tests
OK
```

## Generated Outputs

- `output/raw_data_profile.txt`
- `output/summary_by_commodity.csv`
- `output/summary_by_market.csv`
- `output/price_change_summary.csv`
- `output/price_spikes.csv`
- `output/charts/highest_average_prices.png`
- `output/charts/price_trends.png`
- `output/final_audit.txt`

## Project Structure

- `data_loader.py`: loading and profiling
- `data_cleaning.py`: normalization, conversion, and cleaning
- `filters.py`: reusable filters
- `summaries.py`: grouped statistics, monthly changes, and spike detection
- `visualizations.py`: charts
- `analysis.py`: orchestration and exports
- `main.py`: reproducible command-line entry point
- `tests/test_analysis.py`: deterministic tests

## Reproducibility

A fresh clone of the public GitHub repository was verified in an isolated virtual environment. Dependencies installed from `requirements.txt`, generated artifacts were removed, the raw checksum passed, all outputs regenerated, expected schemas and row counts matched, charts passed validation, Python files compiled, and all 36 tests passed without manual code corrections.

## Resources

- Dataset: https://data.humdata.org/dataset/wfp-food-prices-for-uganda
- Pandas: https://pandas.pydata.org/docs/
- Matplotlib: https://matplotlib.org/stable/
- Python unittest: https://docs.python.org/3/library/unittest.html

## Demonstration Video

[Watch the Uganda Food Price Explorer demonstration](https://youtu.be/B_MTzY8-m3w)

## Repository

[View the Uganda Food Price Explorer repository](https://github.com/ADBranches/uganda-food-price-explorer)
