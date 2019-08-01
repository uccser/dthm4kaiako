"""Views for POET application."""

from ipware import get_client_ip
from django.http import HttpResponseRedirect
from django.views import generic
from django.forms import ValidationError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic.edit import FormView
from poet.forms import POETSurveySelectorForm, POETSurveyForm
from poet.utils import select_resources_for_poet_form
from poet.models import Submission, ProgressOutcome, Resource


class HomeView(FormView):
    template_name = 'poet/home.html'
    form_class = POETSurveySelectorForm
    success_url = reverse_lazy('poet:form')

    def get_context_data(self, **kwargs):
        """Provide the context data for the POET home view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['active_survey'] = self.request.session.get('poet_form_resources', False)
        return context

    def form_valid(self, form):
        """Send email if form is valid."""
        resources_pks = select_resources_for_poet_form(form.cleaned_data['po_group'])
        self.request.session['poet_form_resources'] = resources_pks
        self.request.session['poet_form_new'] = True
        self.request.session['poet_form_active'] = True
        return super().form_valid(form)


def poet_form(request):
    """View for POET form."""
    # Create form view with resources in forms
    context = dict()
    template = 'poet/form.html'

    if request.method == 'POST' and request.session.get('poet_form_active', False):
        form = POETSurveyForm()

        # Check whether POST data is valid, if not return to home
        try:
            form.add_fields_from_request(request)
        except (ObjectDoesNotExist, ValidationError) as e:
            messages.error(request, 'Invalid form data. Returning to POET home.')
            # Delete session data
            request.session.pop('poet_form_resources', None)
            request.session.pop('poet_form_active', None)
            return redirect(reverse('poet:home'))

        context['form'] = form

        # Valid form but missing data
        try:
            data = form.validate(request)
        except ValidationError as e:
            messages.error(request, '{}.'.format(e.message))
        else:
            # Save submissions to database
            client_ip, is_routable = get_client_ip(request)
            for submission_data in data:
                submission_data['ip_address'] = client_ip
                Submission.objects.create(**submission_data)
            # Delete session data
            request.session.pop('poet_form_resources', None)
            request.session.pop('poet_form_active', None)
            # Render results template
            template = 'poet/result.html'
            form.update_form_with_summary()

    # if a GET (or any other method) we'll create a blank form
    else:
        # Get resources for form
        resource_pks = request.session.get('poet_form_resources', None)
        if not resource_pks:
            return redirect(reverse('poet:home'))

        # Check if new form
        new_form = request.session.pop('poet_form_new', False)
        if not new_form:
            messages.info(request, 'Loaded incomplete survey resources.')

        resources = Resource.objects.filter(pk__in=resource_pks)
        form = POETSurveyForm()
        form.add_fields_from_resources(resources)
        context['form'] = form
    context['progress_outcomes'] = {x.pk: x for x in ProgressOutcome.objects.exclude(learning_area__exact='')}
    return render(request, template, context)
