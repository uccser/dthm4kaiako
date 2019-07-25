"""Views for POET application."""

from django.http import HttpResponseRedirect
from django.views import generic
from django.conf import settings
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
    template_name = 'poet/form.html'
    form_list = [Resource1Form, Resource2Form, Resource3Form]

    def done(self, form_list, **kwargs):
        # TODO: Save data to database
        return HttpResponseRedirect(reverse('poet:home'))

# class FormView(generic.base.TemplateView):
#     """View for POET homepage."""

#     template_name = 'general/contact.html'
#     form_class = ContactForm
#     success_url = reverse_lazy('general:contact-success')

#     def form_valid(self, form):
#         """Send email if form is valid."""
#         form.send_email()
#         return super().form_valid(form)
