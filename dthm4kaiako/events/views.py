"""Views for events application."""

from django.views import generic
from django.utils.timezone import now
from events.models import (
    Event,
    Location,
)


class HomeView(generic.TemplateView):
    """View for event homepage."""

    template_name = 'events/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the event homepage view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        future_events = Event.objects.filter(end__gte=now()).order_by('start')
        context['events'] = future_events[:10]
        context['locations'] = Location.objects.filter(events__in=future_events).distinct()
        return context
