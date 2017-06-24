"""Views for the events application."""

from django.views import generic
from django.db.models import BooleanField, DateField, Value
from django.db.models.aggregates import Max, Min
from django.shortcuts import get_object_or_404
from events.models import (
    Event,
    ThirdPartyEvent,
    Session,
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
        events = Event.objects.filter(
            is_published=True
        ).annotate(
            third_party=Value(False, output_field=BooleanField()),
            start_date=Min("sessions__start_datetime", output_field=DateField()),
            end_date=Max("sessions__end_datetime", output_field=DateField()),
        ).only(
            "slug",
            "name",
        )

        third_party_events = ThirdPartyEvent.objects.filter(
            is_published=True
        ).annotate(
            third_party=Value(True, output_field=BooleanField()),
        ).only(
            "slug",
            "name",
            "start_date",
            "end_date",
        )

        return events.union(third_party_events).order_by(
            "start_date",
            "end_date"
        )


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
        context["sessions"] = self.object.sessions.order_by("start_datetime", "end_datetime")
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
