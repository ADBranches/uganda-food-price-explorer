"""URL routes for the explorer application."""

from django.urls import path

from . import views

app_name = "explorer"

urlpatterns = [
    path("", views.home, name="home"),
    path("explorer/", views.explorer, name="explorer"),
    path("results/", views.results, name="results"),
]
