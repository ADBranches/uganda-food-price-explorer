"""Views for the Uganda Food Price Explorer web application."""

from django.shortcuts import render


def home(request):
    """Render the home page and current application status."""
    context = {
        "page_title": "Uganda Food Price Explorer",
        "active_page": "home",
        "status_message": "The Django web application foundation is running successfully.",
    }
    return render(request, "explorer/home.html", context)


def explorer(request):
    """Render the page reserved for interactive dataset filters."""
    context = {
        "page_title": "Explorer | Uganda Food Price Explorer",
        "active_page": "explorer",
    }
    return render(request, "explorer/explorer.html", context)


def results(request):
    """Render the page reserved for dynamically generated results."""
    context = {
        "page_title": "Results | Uganda Food Price Explorer",
        "active_page": "results",
    }
    return render(request, "explorer/results.html", context)
