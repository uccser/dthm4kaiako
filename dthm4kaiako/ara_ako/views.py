"""Views for Ara Ako application."""

from django.views import generic
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now
from ara_ako.models import AraAkoEvent
from events.utils import organise_schedule_data


class AraAkoHomeView(generic.ListView):
    """View for Ara Ako homepage."""

    model = AraAkoEvent
    template_name = 'ara_ako/home.html'
    context_object_name = 'ara_ako_events'

    def get_queryset(self):
        """Only show published events.

        Returns:
            Ara Ako events filtered by published boolean.
        """
        return AraAkoEvent.objects.filter(published=True)


class AraAkoEventDetailView(generic.DetailView):
    """View for a specific Ara Ako event."""

    model = AraAkoEvent
    context_object_name = 'ara_ako_event'
    template_name = 'ara_ako/event.html'


class AraAkoDashboardView(generic.DetailView):
    """View for a dashboard for an Ara Ako event."""

    model = AraAkoEvent
    context_object_name = 'ara_ako_event'
    template_name = 'ara_ako/dashboard.html'


def dashboard_json(request, **kwargs):
    """Provide JSON data for event dashboard.

    Args:
        request: The HTTP request.

    Returns:
        JSON response is sent containing data for the requested dashboard.
    """
    # If term parameter, then return JSON
    if "slug" in request.GET:
        event_slug = request.GET.get("slug")
        ara_ako_event = get_object_or_404(
            AraAkoEvent,
            slug=event_slug
        )

        # Get sessions
        sessions = ara_ako_event.event.sessions.filter(
            end__gte=now()
        ).prefetch_related(
            'locations'
        )
        # Organise sessions
        context = {
            'schedule': organise_schedule_data(sessions)
        }
        # Render as HTML
        html = render_to_string('events/event_schedule.html', context)
        # Prepare JSON data
        data = {
            "slug": event_slug,
            "schedule_html": html,
        }
        return JsonResponse(data)
    else:
        raise Http404("Event slug parameter not found.")
