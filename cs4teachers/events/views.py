"""Views for the events application."""

from django.views import generic
from events.models import Event


class IndexView(generic.ListView):
    """View for the events application homepage."""

    template_name = "events/index.html"
    context_object_name = "events"

    def get_queryset(self):
        """Get queryset of all topics.

        Returns:
            Queryset of Topic objects ordered by name.
        """
        return Event.objects.filter(is_published=True).order_by("start_date")


class EventView(generic.DetailView):
    """View for a specific event."""

    model = Event
    template_name = "events/event.html"
    slug_url_kwarg = "event_slug"


    def get_context_data(self, **kwargs):
        """Provide the context data for the event view.

        Returns:
            Dictionary of context data.
        """
        context = super(EventView, self).get_context_data(**kwargs)
        context["sessions"] = self.object.sessions.order_by("start_datetime", "end_datetime")
