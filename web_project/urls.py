"""URL configuration for the Uganda Food Price Explorer web project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("explorer.urls")),
]
