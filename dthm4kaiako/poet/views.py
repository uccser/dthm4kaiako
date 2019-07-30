"""Views for POET application."""

from django.http import HttpResponseRedirect
from django.views import generic
from django.forms import ValidationError
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from poet.forms import POETForm
from poet.utils import select_resources_for_poet_form
from poet.models import Submission


class HomeView(generic.base.TemplateView):
    """View for POET homepage."""

    template_name = 'poet/home.html'


def poet_form(request):
    """View for POET form."""
    # Create form view with resources in forms
    context = dict()
    template = 'poet/form.html'

    if request.method == 'POST' and not request.session.get('poet_form_submitted', False):
        # Check whether POST data is valid
        form = POETForm()
        try:
            form.add_fields_from_request(request)
        except (ObjectDoesNotExist, ValidationError) as e:
            messages.error(request, '{}. Returning to POET home.'.format(e.message))
            redirect(reverse('poet:home'))

        context['form'] = form

        try:
            data = form.validate(request)
        except ValidationError as e:
            messages.error(request, '{}.'.format(e.message))
        else:
            # Save submissions to database
            print(data)
            for submission_data in data:
                Submission.objects.create(**submission_data)
            # Render results template with form.cleaned_data
            request.session['poet_form_submitted'] = True
            template = 'poet/result.html'
            form.update_form_with_summary()

    # if a GET (or any other method) we'll create a blank form
    else:
        # Get resources for form
        # TODO: Add picking logic based off user request
        resources = select_resources_for_poet_form(request)
        form = POETForm()
        form.add_fields_from_resources(resources)
        pks = list()
        for resource in resources:
            pks.append(resource.pk)
        request.session['poet_form_resources'] = pks
        request.session['poet_form_submitted'] = False
        context['form'] = form

    return render(request, template, context)
