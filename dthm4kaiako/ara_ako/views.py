"""Views for Ara Ako application."""

from django.views import generic


class HomeView(generic.TemplateView):
    """View for event homepage."""

    template_name = 'ara_ako/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the event homepage view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        return context
