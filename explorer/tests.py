"""Layout and navigation tests for the explorer Django application."""

from django.test import TestCase
from django.urls import reverse


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
