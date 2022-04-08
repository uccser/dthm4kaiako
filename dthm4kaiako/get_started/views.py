"""Views for events application."""

from django.views import generic
from get_started.models import Component


class HomeView(generic.ListView):
    """View for Get Started homepage."""

    model = Component
    template_name = 'get_started/home.html'
    context_object_name = 'components'

    def get_queryset(self):
        """Only show published events.

        Returns:
            Ara Ako events filtered by published boolean.
        """
        return Component.objects.exclude(visibility=Component.VISIBILITY_HIDDEN)


class ComponentDetailView(generic.DetailView):
    """View for a specific Get Started component."""

    model = Component
    context_object_name = 'component'
