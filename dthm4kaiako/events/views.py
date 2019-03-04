"""Views for events application."""

from django.views import generic
from django.utils.timezone import now
from events.models import (
    Event,
)

class HomeView(generic.ListView):
    """View for event homepage."""

    template_name = 'events/home.html'
    context_object_name = "events"

    def get_queryset(self):
        """Get queryset of all upcoming events.

        Returns:
            Queryset of Event objects ordered by start datetime.
        """
        return Event.objects.filter(end__gte=now()).order_by('start')[:10]
