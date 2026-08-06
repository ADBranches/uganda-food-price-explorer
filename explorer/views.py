"""Views for the Uganda Food Price Explorer web application."""

from django.shortcuts import render


def home(request):
    """Render the application home page."""
    context = {
        "page_title": "Uganda Food Price Explorer",
        "status_message": "The Django web application foundation is running successfully.",
    }
    return render(request, "explorer/base.html", context)
