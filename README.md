# Overview

## Uganda Food Price Explorer

Uganda Food Price Explorer is a Python data-analysis project that examines historical food-price records from markets across Uganda. The project uses the Uganda Food Prices dataset published by the World Food Programme through the Humanitarian Data Exchange:

https://data.humdata.org/dataset/wfp-food-prices-for-uganda

The dataset contains 32,115 records collected between January 2006 and June 2026. It covers 38 commodities, 43 markets and five measurement units. I selected this dataset because food-price changes affect household purchasing decisions, market planning and food-security discussions. The dataset also provided a practical opportunity to work with dates, prices, categories, markets, missing values, measurement units and repeated observations.

My goal was to learn how to build a complete and reproducible data-analysis workflow with Python. The project helped me practise loading and profiling a CSV file, cleaning data, converting data types, applying filters, calculating grouped statistics, identifying monthly price changes, creating charts, testing analytical functions and communicating the limitations of the results.

[Software Demo Video](https://youtu.be/B_MTzY8-m3w)

# Data Analysis Results

## Question 1

**Which commodities and markets have the highest average reported prices, and how do the results change when the dataset is filtered by date, commodity or market?**

The commodity summary groups records by commodity and measurement unit. The market summary groups records by market, commodity and unit. Each summary reports the number of records, mean price, minimum price and maximum price.

The analysis found that Fish (dry) had the highest average reported price among commodities measured in kilograms. The average price was approximately UGX 20,358 per kilogram across 725 records. The complete commodity summary contains 38 rows, while the market summary contains 638 market, commodity and unit combinations.

The application supports inclusive date filtering and case-insensitive filtering by commodity and market. Applying these filters recalculates the summaries using only the matching records. Measurement units remain part of every grouping key so values recorded in kilograms, litres, packets or other units are not treated as directly comparable.

## Question 2

**Which commodities show the largest price increases over time, and during which months do unusual upward price changes appear?**

The application converts each observation date into a monthly period and groups the data by commodity, market, measurement unit and month. It then calculates each group record count, monthly average price, previous observed monthly average, absolute change and percentage change.

The analysis produced 31,320 monthly price-change records. A total of 2,759 records met the project upward price-spike rule. The exported results allow price changes to be reviewed by commodity, market, unit and month.

For this project, an upward price spike is defined as a monthly percentage increase of at least 25 percent. The boundary is inclusive, meaning that an increase of exactly 25 percent qualifies while an increase of 24.99 percent does not. This threshold is a consistent classification rule for the analysis. It does not prove that an economic shock occurred or explain the cause of a price change.

The monthly data is sparse. Every commodity, market, unit and month group contains fewer than three source observations. This means that individual observations may have a large effect on monthly averages and percentage changes. The spike results should therefore be interpreted as signals for further investigation rather than definitive evidence of unusual market conditions.

# Development Environment

The project was developed on Kali Linux using Visual Studio Code, Git, GitHub and the command line. Python 3.13 was used to implement and test the application. The project is organized into separate modules for data loading, cleaning, filtering, summarization, visualization, workflow coordination and automated testing.

Python provides the core programming language and standard-library tools used by the application. Pandas is used to load CSV data, convert dates and prices, filter records, group observations, calculate statistics and export analysis results. Matplotlib is used to generate the bar chart and monthly trend chart. Pillow is used during output validation to inspect the generated image files and confirm their dimensions. The unittest framework is used to run 36 automated tests covering data loading, cleaning, conversion, filtering, aggregation, sorting, monthly changes, spike detection, visualization, command-line behavior and error handling.

Install the required packages with:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

Run the complete analysis with:

```bash
.venv/bin/python main.py
```

Run the automated tests with:

```bash
.venv/bin/python -m unittest tests/test_analysis.py -v
```

# Useful Websites

- [Uganda Food Prices Dataset](https://data.humdata.org/dataset/wfp-food-prices-for-uganda)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

# Future Work

- Add an interactive interface that allows users to select dates, commodities, markets and measurement units without entering command-line arguments.
- Improve spike detection by comparing the fixed threshold with rolling medians, median absolute deviation or other methods that are less sensitive to isolated observations.
- Add support for newer or denser datasets so monthly trends can be calculated from larger samples and interpreted with greater confidence.
