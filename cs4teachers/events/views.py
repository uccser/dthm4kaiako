"""Views for the events application."""

from django.views import generic
from django.shortcuts import get_object_or_404
from events.utils import retrieve_all_events
from events.models import (
    Event,
    Session,
    Location,
    ThirdPartyEvent,
)


class IndexView(generic.ListView):
    """View for the events application homepage."""

    template_name = "events/index.html"
    context_object_name = "events"

    def get_queryset(self):
        """Get queryset of all topics.

        Returns:
            Queryset of Topic objects ordered by name.
        """
        return retrieve_all_events()


class EventView(generic.DetailView):
    """View for a specific event."""

    model = Event
    template_name = "events/event.html"
    slug_url_kwarg = "event_slug"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        """Provide the context data for the session view.

        Returns:
            Dictionary of context data.
        """
        context = super(EventView, self).get_context_data(**kwargs)
        sessions = self.object.sessions.order_by("start_datetime", "end_datetime").prefetch_related("locations")
        context["sessions"] = sessions
        context["locations"] = Location.objects.filter(sessions__in=sessions).order_by("name").distinct()
        return context


class SessionView(generic.DetailView):
    """View for a specific session."""

    model = Session
    template_name = "events/session.html"
    context_object_name = "session"

    def get_object(self, **kwargs):
        """Retrieve object for the session view.

        Returns:
            Session object, or raises 404 error if not found.
        """
        return get_object_or_404(
            self.model.objects.select_related(),
            event__slug=self.kwargs.get("event_slug", None),
            slug=self.kwargs.get("session_slug", None)
        )

    def get_context_data(self, **kwargs):
        """Provide the context data for the session view.

        Returns:
            Dictionary of context data.
        """
        context = super(SessionView, self).get_context_data(**kwargs)
        context["event"] = self.object.event
        context["locations"] = self.object.locations.order_by("name")
        context["resources"] = self.object.resources.order_by("name")
        return context


class LocationView(generic.DetailView):
    """View for a specific location."""

    model = Location
    template_name = "events/location.html"
    slug_url_kwarg = "location_slug"
    context_object_name = "location"


class ThirdPartyEventView(generic.DetailView):
    """View for a specific third party event."""

    model = ThirdPartyEvent
    template_name = "events/third-party-event.html"
    slug_url_kwarg = "event_slug"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        """Provide the context data for the third party event view.

        Returns:
            Dictionary of context data.
        """
        context = super(ThirdPartyEventView, self).get_context_data(**kwargs)
        context["locations"] = self.object.locations.order_by("name")
        return context
