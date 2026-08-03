# Module 2 Data Analysis Requirements Checklist

Project: Uganda Food Price Explorer
Module: Data Analysis
Student: Edwin Kambale

## Final Analysis Questions

1. Which commodities and markets have the highest average reported prices, and how do the results change when the dataset is filtered to a selected date range?
2. Which commodities show the largest price increases over time, and during which months do unusual price spikes appear?

## Common Requirements and Evidence

- [ ] Original student-created software
  - Evidence: application source files and Git history
  - Verification: code review and video walkthrough
- [ ] At least 100 meaningful lines of original code
  - Evidence: analysis.py, data_loader.py, data_cleaning.py, filters.py, summaries.py, visualizations.py, main.py
  - Verification: output/final_audit.txt
- [ ] Useful documentation for every student-written function
  - Evidence: function docstrings in every application Python file
  - Verification: automated abstract-syntax-tree docstring audit
- [ ] Correct, fully populated Data Analysis README at the repository root
  - Evidence: README.md
  - Verification: template, accuracy, spelling, and placeholder audits
- [ ] Public GitHub repository with a meaningful name
  - Evidence: public repository named uganda-food-price-explorer
  - Verification: incognito access and main tracking origin/main
- [ ] Four-to-five-minute demonstration video
  - Evidence: video URL in README.md and Module Submission document
  - Verification: presenter visible, software demonstration present, detailed code walkthrough present
- [ ] Video link posted in the Data Analysis Microsoft Teams channel
  - Evidence: completed Teams post
  - Verification: refreshed post and retained screenshot
- [ ] Learning Strategies discussion completed
  - Evidence: submitted course discussion and docs/reflection.md
  - Verification: submission is visible
- [ ] At least 20 genuine hours documented
  - Evidence: /home/trovas/Downloads/projects/byupw/block4_2026/CSE310/module2_time_log.md
  - Verification: no missing, overlapping, unsupported, or unfinished entries
- [ ] Official Module Submission Word document completed
  - Evidence: document downloaded from the official form
  - Verification: links, checklists, time log, reflection, and placeholder audit

## Data Analysis Requirements and Evidence

- [x] Free, publicly usable dataset
  - Evidence: data/raw/uganda_food_prices_raw.csv and docs/dataset_source.md
  - Verification: publisher, URL, access date, reuse terms, fields, and description documented
- [ ] Statistics or data-analysis library
  - Evidence: Pandas usage in source files and pandas in requirements.txt
  - Verification: import and runtime checks
- [ ] Two original analysis questions answered
  - Evidence: questions above, analysis.py, output tables, charts, and README findings
  - Verification: each question has reproducible statistical and visual evidence
- [ ] Data filtering demonstrated
  - Evidence: filters.py
  - Verification: tests for date, commodity, market, combined filters, reversed dates, and empty results
- [ ] Sorting demonstrated
  - Evidence: summaries.py
  - Verification: tests confirm descending rankings by average price and price change
- [ ] Aggregation demonstrated
  - Evidence: summaries.py
  - Verification: tests confirm count, mean, minimum, maximum, monthly averages, and percentage change
- [ ] Data conversion demonstrated
  - Evidence: data_cleaning.py
  - Verification: tests confirm date and numeric conversion, label normalization, duplicate removal, and invalid-row handling
- [ ] Original dataset preserved
  - Evidence: data/raw/uganda_food_prices_raw.csv
  - Verification: cleaning writes only to data/cleaned/uganda_food_prices_cleaned.csv
- [ ] Incompatible units handled honestly
  - Evidence: unit included in relevant grouping keys
  - Verification: tests confirm different units are not compared as equivalent
- [ ] Readable charts produced
  - Evidence: output/charts/highest_average_prices.png and output/charts/price_trends.png
  - Verification: non-empty, labeled, readable, and linked to the questions
- [ ] Reproducible output tables produced
  - Evidence: output/summary_by_commodity.csv, output/summary_by_market.csv, output/price_change_summary.csv, output/price_spikes.csv
  - Verification: clean run regenerates every output
- [ ] Single reproducible entry point
  - Evidence: main.py
  - Verification: python3 main.py regenerates cleaned data, tables, and charts
- [ ] Automated tests included
  - Evidence: tests/test_analysis.py
  - Verification: verbose test run passes without changing production data

## Deliverable Map

### Source Files

- data_loader.py: CSV loading and profiling
- data_cleaning.py: cleaning and type conversion
- filters.py: date, commodity, and market filtering
- summaries.py: grouping, sorting, aggregation, price change, and spike detection
- visualizations.py: bar and time-series charts
- analysis.py: analysis orchestration and exports
- main.py: reproducible command-line entry point

### Tests

- tests/test_analysis.py: loading, cleaning, conversion, filters, sorting, aggregation, changes, spikes, empty results, and invalid input

### Outputs

- output/raw_data_profile.txt: raw schema and quality evidence
- output/summary_by_commodity.csv: Question 1 commodity evidence
- output/summary_by_market.csv: Question 1 market evidence
- output/price_change_summary.csv: Question 2 trend evidence
- output/price_spikes.csv: Question 2 spike evidence
- output/charts/highest_average_prices.png: Question 1 visual evidence
- output/charts/price_trends.png: Question 2 visual evidence
- output/final_audit.txt: syntax, size, docstring, data-quality, and chart audits

### Documentation

- README.md: complete public documentation
- docs/dataset_source.md: provenance and reuse information
- docs/reflection.md: learning-strategies reflection
- docs/video_outline.md: timed video plan
- docs/requirements_checklist.md: this acceptance checklist

### Video Segments

- 0:00-0:30: purpose, dataset, and two questions
- 0:30-1:45: run analysis and show generated outputs
- 1:45-2:30: filtering, sorting, aggregation, and conversion
- 2:30-3:30: findings and charts
- 3:30-4:35: source-code and test walkthrough
- 4:35-5:00: README, public GitHub, limitations, and conclusion

## Phase 1 Completion Gate

- [x] Every common requirement has an evidence location
- [x] Every Data Analysis requirement has an evidence location
- [x] Both analysis questions are explicit and measurable
- [x] No requirement is marked unmapped
- [x] The checklist contains no placeholder instructions
