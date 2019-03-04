"""Views for events application."""

from django.views import generic


class HomeView(generic.base.TemplateView):
    """View for event homepage."""

    template_name = 'events/home.html'
