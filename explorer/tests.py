"""Foundation tests for the explorer Django application."""

from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    """Verify the initial home route and template response."""

    def test_home_route_returns_success(self):
        """Confirm that the home route responds successfully."""
        response = self.client.get(reverse("explorer:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explorer/base.html")
        self.assertContains(response, "Django web application foundation is running successfully.")
