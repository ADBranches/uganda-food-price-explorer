# Project Reflection

## What I Learned

This project strengthened my ability to turn a public dataset into a complete, reproducible analysis. I separated loading, cleaning, filtering, aggregation, visualization, orchestration, and testing into focused modules.

I also learned that technically correct statistics can be misleading without context. Keeping units in grouping keys prevented invalid comparisons, while retaining record counts exposed small samples. The audit showed that every commodity-market-unit-month group had fewer than three observations, which changed how I communicated spike results.

## Problem-Solving Approach

I implemented the project in phases and used targeted tests before the complete suite. Small deterministic DataFrames verified inclusive filters, case-insensitive matching, grouped statistics, percentage changes, and the exact 25 percent spike boundary.

When shell quoting errors and duplicate tests appeared, I inspected current files before applying narrow corrections. Checksums and temporary workspaces protected production data.

## Reproducibility

The finished workflow runs from one command and reports source, row counts, filters, findings, and outputs. A fresh GitHub clone was tested in an isolated environment. Dependencies installed, generated artifacts were removed, all outputs regenerated without code corrections, and all 36 tests passed.

## Future Improvements

With denser observations, I would add robust spike methods using rolling medians, median absolute deviation, or confidence intervals. I would also add an interactive interface for selecting dates, commodities, markets, and units.

## Final Outcome

The project demonstrates loading, conversion, cleaning, filtering, grouping, aggregation, sorting, charting, automated testing, auditing, and reproducibility. The most important lesson is that reliable analysis needs correct computation and honest communication about the limits of the data.
