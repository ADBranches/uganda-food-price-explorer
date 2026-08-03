"""Tests for Uganda Food Price Explorer loading, profiling, and cleaning."""

from __future__ import annotations

import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import pandas as pd

from main import build_parser, main
from data_cleaning import (
    clean_food_price_data,
    convert_dates,
    convert_prices,
    normalize_text_columns,
    normalize_text_value,
    remove_unusable_rows,
    write_cleaned_data,
)
from filters import apply_filters, filter_by_commodity, filter_by_date_range, filter_by_market
from analysis import answer_question_one, answer_question_two
from summaries import calculate_monthly_price_changes, identify_price_spikes, summarize_by_commodity, summarize_by_market
from analysis import create_analysis_charts
from visualizations import create_highest_average_prices_chart, create_price_trends_chart
from data_loader import (
    build_profile_lines,
    count_invalid_prices,
    find_mixed_unit_commodities,
    load_food_price_csv,
    write_profile_report,
)


class DataLoaderTests(unittest.TestCase):
    """Verify raw CSV loading and profiling behavior."""

    def make_sample_frame(self) -> pd.DataFrame:
        """Create a small deterministic food-price frame for profile tests."""
        return pd.DataFrame(
            [
                {"date": "2024-01-15", "market": "Owino", "commodity": "Maize", "unit": "KG", "price": "1200"},
                {"date": "2024-02-15", "market": "Owino", "commodity": "Maize", "unit": "Bag", "price": "90000"},
                {"date": "2024-02-15", "market": "Lira", "commodity": "Beans", "unit": "KG", "price": "0"},
            ]
        )

    def test_load_food_price_csv_requires_existing_file(self) -> None:
        """Verify that missing files produce a readable loading error."""
        with self.assertRaises(FileNotFoundError):
            load_food_price_csv("missing_file.csv")

    def test_load_food_price_csv_requires_expected_columns(self) -> None:
        """Verify that missing analytical fields are rejected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "bad.csv"
            csv_path.write_text("date,market,price\n2024-01-15,Owino,1200\n", encoding="utf-8")
            with self.assertRaises(ValueError) as error:
                load_food_price_csv(csv_path)
            self.assertIn("commodity", str(error.exception))
            self.assertIn("unit", str(error.exception))

    def test_count_invalid_prices_counts_zero_and_non_numeric_values(self) -> None:
        """Verify that zero, negative, and nonnumeric prices are invalid."""
        frame = pd.DataFrame({"price": ["10", "0", "-5", "bad"]})
        self.assertEqual(count_invalid_prices(frame), 3)

    def test_find_mixed_unit_commodities_detects_multiple_units(self) -> None:
        """Verify that commodities observed in multiple units are reported."""
        mixed_units = find_mixed_unit_commodities(self.make_sample_frame())
        self.assertIn("Maize", mixed_units.index)
        self.assertEqual(int(mixed_units.loc["Maize"]), 2)

    def test_build_profile_lines_reports_core_dataset_facts(self) -> None:
        """Verify that the profile includes rows, dates, invalid prices, and units."""
        joined = "\n".join(build_profile_lines(self.make_sample_frame()))
        self.assertIn("Row count: 3", joined)
        self.assertIn("Column count: 5", joined)
        self.assertIn("Invalid or non-positive prices: 1", joined)
        self.assertIn("Earliest date: 2024-01-15", joined)
        self.assertIn("Latest date: 2024-02-15", joined)
        self.assertIn("Maize: 2 units", joined)

    def test_write_profile_report_creates_output_file(self) -> None:
        """Verify that the profile report is written to disk."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "profile.txt"
            result_path = write_profile_report(self.make_sample_frame(), output_path)
            self.assertEqual(result_path, output_path)
            self.assertTrue(output_path.exists())
            self.assertIn("Uganda Food Price Raw Dataset Profile", output_path.read_text())


class DataCleaningTests(unittest.TestCase):
    """Verify the reproducible cleaning pipeline."""

    def make_dirty_frame(self) -> pd.DataFrame:
        """Create deterministic dirty records for cleaning tests."""
        duplicate = {
            "date": "2024-01-15",
            "market": "  Owino  Market ",
            "commodity": "  Maize   Flour ",
            "unit": " KG ",
            "price": "1200",
            "category": " cereals and tubers ",
        }
        return pd.DataFrame(
            [
                duplicate,
                duplicate.copy(),
                {"date": "bad-date", "market": "Lira", "commodity": "Beans", "unit": "KG", "price": "500", "category": "pulses"},
                {"date": "2024-02-15", "market": "Lira", "commodity": "Beans", "unit": "KG", "price": "0", "category": "pulses"},
                {"date": "2024-03-15", "market": "", "commodity": "Rice", "unit": "KG", "price": "3000", "category": "cereal"},
            ]
        )

    def test_normalize_text_value_trims_and_collapses_spaces(self) -> None:
        """Verify whitespace normalization for one text value."""
        self.assertEqual(normalize_text_value("  Maize   Flour  "), "Maize Flour")

    def test_convert_dates_creates_datetime_values(self) -> None:
        """Verify valid dates convert and invalid dates become missing."""
        frame = convert_dates(pd.DataFrame({"date": ["2024-01-15", "not-a-date"]}))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(frame["date"]))
        self.assertEqual(int(frame["date"].isna().sum()), 1)

    def test_convert_prices_creates_numeric_values(self) -> None:
        """Verify valid prices convert and invalid prices become missing."""
        frame = convert_prices(pd.DataFrame({"price": ["1200", "bad"]}))
        self.assertTrue(pd.api.types.is_numeric_dtype(frame["price"]))
        self.assertEqual(int(frame["price"].isna().sum()), 1)

    def test_clean_food_price_data_removes_duplicates_and_invalid_rows(self) -> None:
        """Verify full cleaning removes unusable rows and exact duplicates."""
        cleaned = clean_food_price_data(self.make_dirty_frame())
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned.loc[0, "market"], "Owino Market")
        self.assertEqual(cleaned.loc[0, "commodity"], "Maize Flour")
        self.assertEqual(cleaned.loc[0, "unit"], "KG")
        self.assertEqual(float(cleaned.loc[0, "price"]), 1200.0)

    def test_remove_unusable_rows_requires_analysis_fields(self) -> None:
        """Verify only rows with usable date, labels, unit, and positive price remain."""
        frame = convert_prices(convert_dates(normalize_text_columns(self.make_dirty_frame())))
        cleaned = remove_unusable_rows(frame)
        self.assertTrue((cleaned["price"] > 0).all())
        self.assertTrue(cleaned["date"].notna().all())
        self.assertTrue(cleaned[["market", "commodity", "unit"]].ne("").all().all())

    def test_write_cleaned_data_creates_iso_date_csv(self) -> None:
        """Verify cleaned output is written with ISO date strings."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "cleaned.csv"
            cleaned = clean_food_price_data(self.make_dirty_frame())
            write_cleaned_data(cleaned, output_path)
            text = output_path.read_text(encoding="utf-8")
            self.assertIn("2024-01-15", text)
            self.assertIn("Owino Market", text)


class ReusableFilterTests(unittest.TestCase):
    """Verify date, commodity, market, combined, and non-mutating filters."""

    def make_filter_frame(self) -> pd.DataFrame:
        """Create deterministic rows used by reusable-filter tests."""
        return pd.DataFrame(
            [
                {"date": "2024-01-15", "market": "Owino", "commodity": "Maize", "unit": "KG", "price": 1000.0},
                {"date": "2024-02-15", "market": "Lira", "commodity": "Beans", "unit": "KG", "price": 2000.0},
                {"date": "2024-03-15", "market": "Owino", "commodity": "Beans", "unit": "KG", "price": 2500.0},
            ]
        )

    def test_date_filter_is_inclusive(self) -> None:
        """Verify that records on both date boundaries are included."""
        result = filter_by_date_range(self.make_filter_frame(), "2024-01-15", "2024-02-15")
        self.assertEqual(len(result), 2)
        self.assertEqual(result.iloc[0]["date"], "2024-01-15")
        self.assertEqual(result.iloc[1]["date"], "2024-02-15")

    def test_date_filter_rejects_reversed_range(self) -> None:
        """Verify that a start date after the end date is rejected."""
        with self.assertRaisesRegex(ValueError, "Start date"):
            filter_by_date_range(self.make_filter_frame(), "2024-03-15", "2024-01-15")

    def test_commodity_filter_is_case_insensitive(self) -> None:
        """Verify exact commodity matching ignores case and surrounding spaces."""
        result = filter_by_commodity(self.make_filter_frame(), " beans ")
        self.assertEqual(len(result), 2)
        self.assertTrue(result["commodity"].eq("Beans").all())

    def test_market_filter_is_case_insensitive(self) -> None:
        """Verify exact market matching ignores case and surrounding spaces."""
        result = filter_by_market(self.make_filter_frame(), " owino ")
        self.assertEqual(len(result), 2)
        self.assertTrue(result["market"].eq("Owino").all())

    def test_combined_filters_return_expected_row(self) -> None:
        """Verify that date, commodity, and market constraints work together."""
        result = apply_filters(
            self.make_filter_frame(),
            start_date="2024-02-01",
            end_date="2024-03-31",
            commodity="beans",
            market="owino",
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result.loc[0, "date"], "2024-03-15")

    def test_no_match_returns_documented_empty_frame(self) -> None:
        """Verify that unmatched criteria return an empty DataFrame with the original columns."""
        source = self.make_filter_frame()
        result = apply_filters(source, commodity="Rice")
        self.assertTrue(result.empty)
        self.assertEqual(list(result.columns), list(source.columns))

    def test_filters_do_not_modify_source_frame(self) -> None:
        """Verify that filtering leaves the original DataFrame unchanged."""
        source = self.make_filter_frame()
        original = source.copy(deep=True)
        apply_filters(source, start_date="2024-02-01", commodity="Beans", market="Owino")
        pd.testing.assert_frame_equal(source, original)




class QuestionOneSummaryTests(unittest.TestCase):
    """Verify Question 1 statistics, sorting, unit separation, and exports."""

    def make_summary_frame(self) -> pd.DataFrame:
        """Create known prices for deterministic summary tests."""
        return pd.DataFrame([
            {"date": "2024-01-15", "market": "Owino", "commodity": "Maize", "unit": "KG", "price": 1000.0},
            {"date": "2024-02-15", "market": "Owino", "commodity": "Maize", "unit": "KG", "price": 3000.0},
            {"date": "2024-02-15", "market": "Lira", "commodity": "Beans", "unit": "KG", "price": 5000.0},
            {"date": "2024-03-15", "market": "Lira", "commodity": "Maize", "unit": "Unit", "price": 9000.0},
        ])

    def test_commodity_summary_calculates_statistics_and_sort_order(self) -> None:
        """Verify statistics, unit separation, and descending mean order."""
        result = summarize_by_commodity(self.make_summary_frame())
        self.assertEqual(result.iloc[0]["commodity"], "Maize")
        self.assertEqual(result.iloc[0]["unit"], "Unit")
        maize_kg = result[(result["commodity"] == "Maize") & (result["unit"] == "KG")].iloc[0]
        self.assertEqual(int(maize_kg["record_count"]), 2)
        self.assertEqual(float(maize_kg["mean_price"]), 2000.0)
        self.assertEqual(float(maize_kg["minimum_price"]), 1000.0)
        self.assertEqual(float(maize_kg["maximum_price"]), 3000.0)
        self.assertTrue(result["mean_price"].is_monotonic_decreasing)

    def test_market_summary_preserves_context(self) -> None:
        """Verify market results retain market, commodity, and unit fields."""
        result = summarize_by_market(self.make_summary_frame())
        self.assertEqual(list(result.columns[:3]), ["market", "commodity", "unit"])
        self.assertEqual(len(result), 3)

    def test_question_one_exports_required_tables(self) -> None:
        """Verify both required Question 1 files are exported."""
        with tempfile.TemporaryDirectory() as temp_dir:
            commodity_result, market_result = answer_question_one(self.make_summary_frame(), temp_dir)
            self.assertFalse(commodity_result.empty)
            self.assertFalse(market_result.empty)
            self.assertTrue((Path(temp_dir) / "summary_by_commodity.csv").exists())
            self.assertTrue((Path(temp_dir) / "summary_by_market.csv").exists())

    def test_question_one_applies_date_filter(self) -> None:
        """Verify summaries include only rows inside the requested dates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            commodity_result, market_result = answer_question_one(
                self.make_summary_frame(),
                temp_dir,
                start_date="2024-02-01",
                end_date="2024-02-29",
            )
            self.assertEqual(int(commodity_result["record_count"].sum()), 2)
            self.assertEqual(int(market_result["record_count"].sum()), 2)




class QuestionTwoTrendTests(unittest.TestCase):
    """Verify monthly averages, price changes, spike boundaries, and exports."""

    def make_trend_frame(self) -> pd.DataFrame:
        """Create known monthly records for deterministic trend tests."""
        return pd.DataFrame([
            {"date": "2024-01-05", "market": "Owino", "commodity": "Beans", "unit": "KG", "price": 100.0},
            {"date": "2024-01-20", "market": "Owino", "commodity": "Beans", "unit": "KG", "price": 200.0},
            {"date": "2024-02-10", "market": "Owino", "commodity": "Beans", "unit": "KG", "price": 187.5},
            {"date": "2024-03-10", "market": "Owino", "commodity": "Beans", "unit": "KG", "price": 234.375},
            {"date": "2024-01-10", "market": "Lira", "commodity": "Maize", "unit": "KG", "price": 1000.0},
            {"date": "2024-02-10", "market": "Lira", "commodity": "Maize", "unit": "KG", "price": 1100.0},
        ])

    def test_monthly_averages_and_changes_are_correct(self) -> None:
        """Verify monthly averaging, absolute change, and percentage change."""
        result = calculate_monthly_price_changes(self.make_trend_frame())
        beans = result[
            (result["commodity"] == "Beans")
            & (result["market"] == "Owino")
            & (result["unit"] == "KG")
        ].reset_index(drop=True)

        self.assertEqual(len(beans), 3)
        self.assertEqual(float(beans.loc[0, "monthly_average_price"]), 150.0)
        self.assertTrue(pd.isna(beans.loc[0, "percentage_change"]))
        self.assertEqual(float(beans.loc[1, "absolute_change"]), 37.5)
        self.assertEqual(float(beans.loc[1, "percentage_change"]), 25.0)
        self.assertEqual(float(beans.loc[2, "percentage_change"]), 25.0)

    def test_monthly_groups_preserve_market_commodity_and_unit(self) -> None:
        """Verify monthly calculations keep each time series separate."""
        result = calculate_monthly_price_changes(self.make_trend_frame())

        self.assertEqual(
            list(result.columns[:4]),
            ["commodity", "market", "unit", "month"],
        )
        self.assertEqual(len(result), 5)

    def test_spike_rule_includes_exact_threshold(self) -> None:
        """Verify an increase exactly equal to the threshold is a spike."""
        changes = pd.DataFrame([
            {"commodity": "Beans", "market": "Owino", "unit": "KG", "month": "2024-02", "percentage_change": 25.0},
            {"commodity": "Maize", "market": "Lira", "unit": "KG", "month": "2024-02", "percentage_change": 24.99},
        ])

        spikes = identify_price_spikes(
            changes,
            threshold_percent=25.0,
        ).reset_index(drop=True)

        self.assertEqual(len(spikes), 1)
        self.assertEqual(spikes.loc[0, "commodity"], "Beans")

    def test_spike_rule_rejects_negative_threshold(self) -> None:
        """Verify a negative spike threshold is rejected."""
        with self.assertRaisesRegex(ValueError, "threshold"):
            identify_price_spikes(
                pd.DataFrame(),
                threshold_percent=-1.0,
            )

    def test_question_two_exports_both_tables(self) -> None:
        """Verify Question 2 exports change and spike CSV files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            change_result, spike_result = answer_question_two(
                self.make_trend_frame(),
                output_directory=temp_dir,
                threshold_percent=25.0,
            )

            self.assertFalse(change_result.empty)
            self.assertFalse(spike_result.empty)
            self.assertTrue(
                (Path(temp_dir) / "price_change_summary.csv").exists()
            )
            self.assertTrue(
                (Path(temp_dir) / "price_spikes.csv").exists()
            )




class VisualizationTests(unittest.TestCase):
    """Verify chart creation without mixing measurement units."""

    def make_chart_summary(self) -> pd.DataFrame:
        """Create known commodity summaries for chart tests."""
        return pd.DataFrame([
            {"commodity": "Fish", "unit": "KG", "record_count": 20, "mean_price": 8000.0, "minimum_price": 5000.0, "maximum_price": 10000.0},
            {"commodity": "Beans", "unit": "KG", "record_count": 30, "mean_price": 3000.0, "minimum_price": 2000.0, "maximum_price": 4000.0},
            {"commodity": "Hoe", "unit": "Unit", "record_count": 10, "mean_price": 12000.0, "minimum_price": 9000.0, "maximum_price": 15000.0},
        ])

    def make_trend_summary(self) -> pd.DataFrame:
        """Create known monthly Beans trends for chart tests."""
        return pd.DataFrame([
            {"commodity": "Beans", "market": "Owino", "unit": "KG", "month": "2024-01", "record_count": 4, "monthly_average_price": 2000.0},
            {"commodity": "Beans", "market": "Owino", "unit": "KG", "month": "2024-02", "record_count": 5, "monthly_average_price": 2200.0},
            {"commodity": "Beans", "market": "Lira", "unit": "KG", "month": "2024-01", "record_count": 3, "monthly_average_price": 2100.0},
            {"commodity": "Beans", "market": "Lira", "unit": "KG", "month": "2024-02", "record_count": 3, "monthly_average_price": 2300.0},
        ])

    def test_highest_average_chart_creates_nonempty_png(self) -> None:
        """Verify the single-unit bar chart creates a non-empty PNG."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "highest.png"
            result = create_highest_average_prices_chart(
                self.make_chart_summary(), path, unit="KG", top_n=2
            )
            self.assertEqual(result, path)
            self.assertTrue(path.exists())
            self.assertGreater(path.stat().st_size, 0)

    def test_price_trends_chart_creates_nonempty_png(self) -> None:
        """Verify the single-commodity and single-unit trend chart."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "trends.png"
            result = create_price_trends_chart(
                self.make_trend_summary(),
                path,
                commodity="Beans",
                unit="KG",
                top_markets=2,
            )
            self.assertEqual(result, path)
            self.assertTrue(path.exists())
            self.assertGreater(path.stat().st_size, 0)

    def test_highest_average_chart_rejects_missing_unit(self) -> None:
        """Verify the bar chart rejects a unit with no matching rows."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "No commodity summary rows"):
                create_highest_average_prices_chart(
                    self.make_chart_summary(),
                    Path(temp_dir) / "missing.png",
                    unit="L",
                )

    def test_analysis_chart_workflow_creates_both_files(self) -> None:
        """Verify the integrated chart workflow creates both PNG files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            bar_path, trend_path = create_analysis_charts(
                self.make_chart_summary(),
                self.make_trend_summary(),
                temp_dir,
            )
            self.assertTrue(bar_path.exists())
            self.assertTrue(trend_path.exists())
            self.assertGreater(bar_path.stat().st_size, 0)
            self.assertGreater(trend_path.stat().st_size, 0)




class EntryPointTests(unittest.TestCase):
    """Verify command-line parsing, forwarding, and failure statuses."""

    def test_parser_exposes_reproducible_defaults(self):
        """Verify default paths and spike threshold are deterministic."""
        args = build_parser().parse_args([])

        self.assertEqual(
            args.raw_path,
            "data/raw/uganda_food_prices_raw.csv",
        )
        self.assertEqual(
            args.cleaned_path,
            "data/cleaned/uganda_food_prices_cleaned.csv",
        )
        self.assertEqual(args.output_directory, "output")
        self.assertEqual(args.spike_threshold, 25.0)

    @patch("main.run_complete_analysis")
    def test_main_forwards_configuration_and_returns_zero(
        self,
        mocked_run,
    ):
        """Verify valid CLI arguments reach the complete workflow."""
        status = main(
            [
                "--raw-path",
                "raw.csv",
                "--cleaned-path",
                "cleaned.csv",
                "--output-directory",
                "results",
                "--start-date",
                "2024-01-01",
                "--end-date",
                "2024-12-31",
                "--commodity",
                "Beans",
                "--market",
                "Owino",
                "--spike-threshold",
                "30",
            ]
        )

        self.assertEqual(status, 0)

        mocked_run.assert_called_once_with(
            raw_path="raw.csv",
            cleaned_path="cleaned.csv",
            output_directory="results",
            start_date="2024-01-01",
            end_date="2024-12-31",
            commodity="Beans",
            market="Owino",
            spike_threshold=30.0,
        )

    @patch("main.run_complete_analysis")
    def test_main_returns_nonzero_for_invalid_configuration(
        self,
        mocked_run,
    ):
        """Verify a workflow validation error produces status one."""
        mocked_run.side_effect = ValueError(
            "Spike threshold must be zero or greater."
        )

        status = main(["--spike-threshold", "-1"])

        self.assertEqual(status, 1)

    @patch("main.run_complete_analysis")
    def test_main_returns_nonzero_for_missing_input(
        self,
        mocked_run,
    ):
        """Verify a missing source file produces status one."""
        mocked_run.side_effect = FileNotFoundError(
            "CSV file not found: missing.csv"
        )

        status = main(["--raw-path", "missing.csv"])

        self.assertEqual(status, 1)

if __name__ == "__main__":
    unittest.main()
