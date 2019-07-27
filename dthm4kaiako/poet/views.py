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
