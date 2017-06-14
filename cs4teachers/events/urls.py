"""URL routing for the events application."""

from django.conf.urls import url
from events import views


app_name = "events"
urlpatterns = [
    # eg: /events/
    url(
        r"^$",
        views.IndexView.as_view(),
        name="index"
    ),
    # eg: /events/cs4hs-2017/
    url(
        r"^(?P<event_slug>[-\w]+)/$",
        views.EventView.as_view(),
        name="event"
    ),
]
