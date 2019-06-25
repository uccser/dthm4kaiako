"""Views for POET application."""

from random import randint
from django.views import generic
from django.conf import settings


class HomeView(generic.base.TemplateView):
    """View for POET homepage."""

    template_name = 'poet/home.html'
