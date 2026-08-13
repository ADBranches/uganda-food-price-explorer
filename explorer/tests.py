"""Django tests for shared navigation and the dynamic home page."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd
from django.test import TestCase
from django.urls import reverse

from explorer.views import build_dataset_overview


class SharedLayoutTests(TestCase):
    """Verify the three routes and shared navigation structure."""

    def test_home_route_uses_home_template(self):
        """Confirm that the home route renders through the shared layout."""
        response = self.client.get(reverse("explorer:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explorer/base.html")
        self.assertTemplateUsed(response, "explorer/home.html")
        self.assertContains(response, "Explore historical food prices")

    def test_explorer_route_uses_explorer_template(self):
        """Confirm that the Explorer route renders successfully."""
        response = self.client.get(reverse("explorer:explorer"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explorer/base.html")
        self.assertTemplateUsed(response, "explorer/explorer.html")
        self.assertContains(response, "Explore the dataset")

    def test_results_route_uses_results_template(self):
        """Confirm that the Results route renders successfully."""
        response = self.client.get(reverse("explorer:results"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explorer/base.html")
        self.assertTemplateUsed(response, "explorer/results.html")
        self.assertContains(response, "Analysis results will appear here")

    def test_home_page_contains_navigation_links(self):
        """Confirm that all planned pages are available in navigation."""
        response = self.client.get(reverse("explorer:home"))
        self.assertContains(response, reverse("explorer:home"))
        self.assertContains(response, reverse("explorer:explorer"))
        self.assertContains(response, reverse("explorer:results"))


class DatasetOverviewTests(TestCase):
    """Verify dynamic summary values and readable dataset failures."""

    def test_build_dataset_overview_calculates_values(self):
        """Calculate overview values from a temporary cleaned CSV."""
        frame = pd.DataFrame(
            {
                "date": ["2025-01-01", "2025-02-01", "2025-03-01"],
                "market": ["A", "A", "B"],
                "commodity": ["Beans", "Maize", "Beans"],
                "unit": ["KG", "KG", "L"],
                "price": [1000, 1200, 900],
            }
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "cleaned.csv"
            frame.to_csv(path, index=False)
            overview = build_dataset_overview(path)
        self.assertEqual(overview["record_count"], 3)
        self.assertEqual(overview["commodity_count"], 2)
        self.assertEqual(overview["market_count"], 2)
        self.assertEqual(overview["unit_count"], 2)
        self.assertEqual(overview["start_date"].isoformat(), "2025-01-01")
        self.assertEqual(overview["end_date"].isoformat(), "2025-03-01")

    def test_home_page_displays_real_dataset_overview(self):
        """Display summary values supplied dynamically by the home view."""
        response = self.client.get(reverse("explorer:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "32115")
        self.assertContains(response, "38")
        self.assertContains(response, "43")
        self.assertContains(response, "January 15, 2006")
        self.assertContains(response, "June 15, 2026")

    @patch("explorer.views.CLEANED_DATA_PATH", Path("missing-cleaned-data.csv"))
    def test_home_page_handles_missing_dataset(self):
        """Return HTTP 200 and a readable message when data is missing."""
        response = self.client.get(reverse("explorer:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dataset overview is unavailable")
        self.assertContains(response, "CSV file not found")
