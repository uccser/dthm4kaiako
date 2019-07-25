"""Views for POET application."""

from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from formtools.wizard.views import SessionWizardView
from poet.forms import (
    Resource1Form,
    Resource2Form,
    Resource3Form,
)


class HomeView(generic.base.TemplateView):
    """View for POET homepage."""

    template_name = 'poet/home.html'


class FormWizardView(SessionWizardView):
    """View for POET form."""

    template_name = 'poet/form.html'
    form_list = [Resource1Form, Resource2Form, Resource3Form]

    def done(self, form_list, **kwargs):
        """Call when all pages of form are completed."""
        # TODO: Save data to database
        return HttpResponseRedirect(reverse('poet:home'))
