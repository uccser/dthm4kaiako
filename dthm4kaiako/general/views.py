"""Views for general application."""

from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import (
    TemplateView,
    FormView,
)
from resources.models import Resource
from events.models import Event
from general.forms import ContactForm


class HomeView(TemplateView):
    """View for website homepage."""

    template_name = 'general/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the website home view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['resource_count'] = Resource.objects.filter(published=True).count()
        context['upcoming_events'] = Event.objects.filter(published=True).filter(end__gte=now()).count()
        context['featured_event'] = Event.objects.filter(published=True).filter(featured=True).filter(
            end__gte=now()).prefetch_related(
            'organisers',
            'locations',
            'sponsors',
        ).select_related(
            'series',
        ).first()
        return context


class AboutView(TemplateView):
    """View for website about page."""

    template_name = 'general/about.html'


class ContactView(FormView):
    """View for website contact page."""

    template_name = 'general/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('general:contact-success')

    def form_valid(self, form):
        """Send email if form is valid."""
        form.send_email()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    """View for website for contact success page."""

    template_name = 'general/contact-success.html'


class FAQView(TemplateView):
    """View for website FAQ page."""

    template_name = 'general/faq.html'
