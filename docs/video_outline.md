# Uganda Food Price Explorer Demonstration Video Outline

## Video Requirements

- Target duration: 4 minutes 50 seconds
- Required range: 4 to 5 minutes
- Presenter camera: visible throughout the demonstration
- Repository: https://github.com/ADBranches/uganda-food-price-explorer
- Current full recording: https://youtu.be/HNtln75HTEg

## Timed Demonstration Plan

### 0:00-0:25 | Introduction and Purpose

- Keep the presenter camera visible.
- Introduce the Uganda Food Price Explorer.
- State that the project uses Python, Pandas, and Matplotlib.
- State both analysis questions:
  1. Which commodities and markets have the highest average prices?
  2. When do unusual upward monthly price changes appear?

### 0:25-0:50 | Dataset and Preservation

- Show docs/dataset_source.md or output/raw_data_profile.txt.
- Identify the World Food Programme and Humanitarian Data Exchange.
- Mention 32,115 rows, 38 commodities, 43 markets, and 5 measurement units.
- Mention the preserved raw CSV and SHA-256 checksum.

### 0:50-1:20 | Reproducible Application Run

- Run python3 main.py from the repository root.
- Show the raw, cleaned, and filtered row counts.
- Show the detected spike count and generated output paths.
- Explain that one command performs loading, cleaning, filtering, analysis, exports, and chart generation.

### 1:20-1:55 | Conversion, Cleaning, and Filtering

- Show data_cleaning.py.
- Point out date conversion, numeric price conversion, text normalization, duplicate removal, and invalid-row removal.
- Show filters.py.
- Explain inclusive date filtering and case-insensitive commodity and market matching.

### 1:55-2:25 | Aggregation, Grouping, and Sorting

- Show summaries.py.
- Explain grouping by commodity and unit.
- Explain grouping by market, commodity, and unit.
- Mention record count, mean, minimum, and maximum prices.
- Explain descending sorting and unit-safe comparisons.

### 2:25-2:55 | Question 1 and Bar Chart

- Show output/charts/highest_average_prices.png.
- Explain that the chart compares only KG-based commodities.
- State that dried fish has the highest average KG price, approximately UGX 20,358 from 725 records.
- Point out the title, axes, units, and sample-size labels.

### 2:55-3:30 | Question 2 and Trend Chart

- Explain monthly grouping by commodity, market, unit, and month.
- Explain monthly average, previous average, absolute change, and percentage change.
- State the inclusive spike threshold of at least 25 percent.
- Show output/charts/price_trends.png.
- Mention 31,320 monthly-change rows and 2,759 detected spike rows.

### 3:30-3:55 | Limitations

- State that every monthly group contains fewer than three source observations.
- Explain that monthly changes and spike classifications may be sensitive to individual records.
- Point out that record counts remain visible in tables and charts.
- Clarify that the 25 percent rule does not prove the existence or cause of an economic shock.

### 3:55-4:25 | Automated Tests and Audit

- Run python3 -m unittest tests/test_analysis.py -v.
- Show Ran 36 tests and OK.
- Briefly mention coverage for loading, cleaning, conversion, filters, grouping, sorting, changes, spikes, charts, and invalid configuration.
- Show output/final_audit.txt briefly.

### 4:25-4:50 | README, GitHub, and Conclusion

- Show the completed README.
- Show the public GitHub repository.
- Mention the one-command workflow, generated outputs, documentation, tests, and reproducibility evidence.
- Conclude the demonstration while keeping the presenter camera visible.

## Rubric Coverage Audit

- Introduction and purpose: 0:00-0:25
- Both analysis questions: 0:00-0:25
- Dataset and source: 0:25-0:50
- Live application run: 0:50-1:20
- Conversion and cleaning: 1:20-1:55
- Filtering: 1:20-1:55
- Aggregation and sorting: 1:55-2:25
- Question 1 and bar chart: 2:25-2:55
- Question 2 and trend chart: 2:55-3:30
- Findings and limitations: 2:25-3:55
- Code walkthrough: 1:20-3:30
- Automated tests and audit: 3:55-4:25
- README and GitHub conclusion: 4:25-4:50
- Presenter camera visible: throughout

## Rehearsal Gate

- Planned duration: 4 minutes 50 seconds
- Minimum allowed duration: 4 minutes
- Maximum allowed duration: 5 minutes
- Every assessed requirement has a specific segment.
