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
    # eg: /events/third-party/wellington-cs4hs-2017/
    url(
        r"^third-party/(?P<event_slug>[-\w]+)/$",
        views.ThirdPartyEventView.as_view(),
        name="third_party_event"
    ),
    # eg: /events/cs4hs-2017/welcome
    url(
        r"^(?P<event_slug>[-\w]+)/(?P<session_slug>[-\w]+)/$",
        views.SessionView.as_view(),
        name="session"
    ),
]
