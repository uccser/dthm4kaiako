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
    # eg: /events/resources/
    url(
        r"^resources/$",
        views.ResourceList.as_view(),
        name="resources"
    ),
    # eg: /events/cs4hs-2017/
    url(
        r"^(?P<event_slug>[-\w]+)/$",
        views.EventView.as_view(),
        name="event"
    ),
    # eg: /events/series/cs4ps/
    url(
        r"^series/(?P<series_slug>[-\w]+)/$",
        views.SeriesView.as_view(),
        name="series"
    ),
    # eg: /events/location/erskine-315/
    url(
        r"^location/(?P<location_slug>[-\w]+)/$",
        views.LocationView.as_view(),
        name="location"
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
