"""Views for POET application."""

from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import render
from poet.forms import ResourceForm
from poet.utils import select_resources_for_poet_form


class HomeView(generic.base.TemplateView):
    """View for POET homepage."""

    template_name = 'poet/home.html'


def poet_form(request):
    """View for POET form."""
    # Create form view with resources in forms
    context = dict()
    template = 'poet/form.html'

    if request.method == 'POST':
        # Check whether POST data is valid, otherwise recreate form
        form = ResourceForm()
        form.add_fields_from_request(request)

        # print(form.is_valid())
        # print(request.POST)
        # print(request.session['poet_form_resources'])
        if True:
            # Render results template with form.cleaned_data
            template = 'poet/result.html'
            form.update_form_with_summary()
        context['form'] = form

    # if a GET (or any other method) we'll create a blank form
    else:
        # Get resources for form
        # TODO: Add picking logic based off user request
        resources = select_resources_for_poet_form(request)
        form = ResourceForm()
        form.add_fields_from_resources(resources)
        pks = list()
        for resource in resources:
            pks.append(resource.pk)
        request.session['poet_form_resources'] = pks
        context['form'] = form

    return render(request, template, context)
