# Dataset Source

## Dataset Identity

- Title: Uganda - Food Prices
- Publisher: WFP - World Food Programme
- Platform: Humanitarian Data Exchange (HDX)
- Dataset page: https://data.humdata.org/dataset/wfp-food-prices-for-uganda
- CSV resource: https://data.humdata.org/dataset/883929b1-521e-4834-97f5-0ccc2df75b89/resource/e082d683-cad5-4dcd-bf54-db76ae254d33/download/wfp_food_prices_uga.csv
- License: Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO)
- Access date: 2026-08-02

## Description

This dataset contains historical food-price observations for Uganda. Records include temporal, market, commodity, unit, currency, and price fields. The project uses the dataset to compare average reported prices and analyze monthly price changes.

## Required Analytical Fields

- date: observation date
- market: market or location
- commodity: reported item
- unit: measurement unit
- price: reported price

## Analytical Suitability

The dataset supports Question 1 because it contains multiple commodities, markets, units, dates, and reported prices. The dataset supports Question 2 because repeated dated observations allow monthly averages, percentage changes, and unusual price spikes to be calculated.

## Raw-Data Preservation

The original download is stored at data/raw/uganda_food_prices_raw.csv. The raw file will not be edited. A SHA-256 checksum is stored at data/raw/uganda_food_prices_raw.csv.sha256 so later phases can verify that the source data remains unchanged.
