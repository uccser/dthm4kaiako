"""Views for the general application."""

from django.views.generic import TemplateView
from events.models import Event

class GeneralIndexView(TemplateView):
    """View for the homepage that renders from a template."""

    template_name = "general/index.html"

    def get_context_data(self, **kwargs):
        """Provide the context data for the homepage.

        Returns:
            Dictionary of context data.
        """
        # Call the base implementation first to get a context
        context = super(GeneralIndexView, self).get_context_data(**kwargs)
        context["upcoming_events"] = Event.objects.filter(is_published=True).order_by("start_date")[:5]
        return context
