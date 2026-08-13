"""Tests for the interactive Explorer filter form."""

from django.test import TestCase
from django.urls import reverse


class ExplorerFormTests(TestCase):
    """Verify dataset choices, validation, and submission behavior."""

    def test_explorer_page_contains_dataset_choices(self):
        """Load commodity, market, and unit choices from the cleaned data."""
        response = self.client.get(reverse("explorer:explorer"))
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn(("Beans", "Beans"), form.fields["commodity"].choices)
        self.assertIn(("Owino", "Owino"), form.fields["market"].choices)
        self.assertIn(("KG", "KG"), form.fields["unit"].choices)
        self.assertEqual(len(form.fields["commodity"].choices), 39)
        self.assertEqual(len(form.fields["market"].choices), 44)
        self.assertEqual(len(form.fields["unit"].choices), 6)

    def test_valid_submission_reaches_results(self):
        """Forward valid and preserved filter values to the Results page."""
        response = self.client.get(reverse("explorer:results"), {"commodity": "Beans", "market": "Owino", "unit": "KG", "start_date": "2020-01-01", "end_date": "2021-12-31", "spike_threshold": "25"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explorer/results.html")
        self.assertContains(response, "Beans")
        self.assertContains(response, "Owino")
        self.assertContains(response, "25.0%")

    def test_reversed_dates_are_rejected(self):
        """Return a clear error when the start date follows the end date."""
        response = self.client.get(reverse("explorer:results"), {"start_date": "2025-12-31", "end_date": "2025-01-01", "spike_threshold": "25"})
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "explorer/explorer.html")
        self.assertContains(response, "Start date must be on or before end date.", status_code=400)

    def test_negative_threshold_is_rejected(self):
        """Return a field error for a negative spike threshold."""
        response = self.client.get(reverse("explorer:results"), {"spike_threshold": "-1"})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Ensure this value is greater than or equal to 0.", status_code=400)
