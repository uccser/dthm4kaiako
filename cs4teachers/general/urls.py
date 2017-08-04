"""URL routing for the general application."""

from django.conf.urls import include, url
from general import views

urlpatterns = [
    url(r"^$", views.GeneralIndexView.as_view(), name="home"),
    url(r"^pages/", include("django.contrib.flatpages.urls")),
]
