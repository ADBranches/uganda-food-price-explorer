# Dataset Source

## Dataset Identity

- **Title:** Uganda - Food Prices
- **Publisher:** World Food Programme
- **Platform:** Humanitarian Data Exchange
- **Dataset page:** https://data.humdata.org/dataset/wfp-food-prices-for-uganda
- **CSV resource:** https://data.humdata.org/dataset/883929b1-521e-4834-97f5-0ccc2df75b89/resource/e082d683-cad5-4dcd-bf54-db76ae254d33/download/wfp_food_prices_uga.csv
- **License:** Creative Commons Attribution for Intergovernmental Organisations, CC BY-IGO
- **Access date:** August 2, 2026

## Description

The dataset contains historical Ugandan food-price observations, including dates, markets, commodities, measurement units, currency, and prices. The project ranks average prices and calculates monthly price changes.

## Verified Profile

- Rows: 32,115
- Columns: 16
- Earliest observation: January 15, 2006
- Latest observation: June 15, 2026
- Commodities: 38
- Markets: 43
- Units: KG, L, Packet, Pair, and Unit
- Missing raw values: 0
- Duplicate raw rows: 0
- Invalid or non-positive raw prices: 0
- Commodities using multiple units: 0

## Analytical Fields

- `date`: observation date
- `market`: market or location
- `commodity`: reported item
- `unit`: measurement unit
- `price`: reported price

## Preservation

The original download is stored at `data/raw/uganda_food_prices_raw.csv` and is never overwritten. Its checksum is stored at `data/raw/uganda_food_prices_raw.csv.sha256`. Cleaning writes to `data/cleaned/uganda_food_prices_cleaned.csv`.

## Limitations

Every exported commodity-market-unit-month group contains fewer than three observations. Monthly changes and spike classifications may therefore be sensitive to individual reports. Record counts remain visible and results are separated by unit.
