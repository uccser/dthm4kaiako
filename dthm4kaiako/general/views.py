"""Views for general application."""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """View for website homepage."""

    template_name = 'general/home.html'


class AboutView(TemplateView):
    """View for website about page."""

    template_name = 'general/about.html'


class ContactView(TemplateView):
    """View for website contact page."""

    template_name = 'general/contact.html'


class FAQView(TemplateView):
    """View for website FAQ page."""

    template_name = 'general/faq.html'
