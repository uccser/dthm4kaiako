"""URL routing for the general application."""

from django.conf.urls import url
from general import views

urlpatterns = [
    url(r"^$", views.GeneralIndexView.as_view(), name="home"),
]
