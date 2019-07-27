"""Views for POET application."""

from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from poet.forms import ResourceForm
from poet.utils import select_resources_for_poet_form


class HomeView(generic.base.TemplateView):
    """View for POET homepage."""

    template_name = 'poet/home.html'


def poet_form(request):
    # Create form view with resources in forms
    context = dict()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ResourceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(request.POST)
            print(request.session['poet_form_resources'])
            return HttpResponseRedirect(reverse('poet:home'))

    # if a GET (or any other method) we'll create a blank form
    else:
        # Get resources for form
        # TODO: Add picking logic based off user request
        resources = select_resources_for_poet_form(request)
        form = ResourceForm()
        form.add_resources(resources)
        pks = list()
        for resource in resources:
            pks.append(resource.pk)
        request.session['poet_form_resources'] = pks
        context['form'] = form

    return render(request, 'poet/form.html', context)


# class FormWizardView(SessionWizardView):
#     """View for POET form."""

#     template_name = 'poet/form.html'
#     form_list = [Resource1Form, Resource2Form, Resource3Form]

#     def get_context_data(self, form, **kwargs):
#         context = super().get_context_data(form=form, **kwargs)

#         return context

#     def done(self, form_list, **kwargs):
#         """Call when all pages of form are completed."""
#         # TODO: Save data to database
#         for form in form_list:
#             print(form.cleaned_data)
#         return HttpResponseRedirect(reverse('poet:home'))
