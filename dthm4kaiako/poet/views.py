"""Views for POET application."""

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
        # self.request.session['poet_form_submitted'] = False
        return super().form_valid(form)


def poet_form(request):
    """View for POET form."""
    # Create form view with resources in forms
    context = dict()
    template = 'poet/form.html'

    if request.method == 'POST' and not request.session.get('poet_form_submitted', False):
        # Check whether POST data is valid
        form = POETSurveyForm()
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
            for submission_data in data:
                Submission.objects.create(**submission_data)
            # Delete session data
            request.session.pop('poet_form_resources', None)
            # Render results template
            request.session['poet_form_submitted'] = True
            template = 'poet/result.html'
            form.update_form_with_summary()

    # if a GET (or any other method) we'll create a blank form
    else:
        # Check if new form
        new_form = request.session.pop('poet_form_new', False)
        if not new_form:
            messages.info(request, 'Loaded incomplete survey resources.')

        # Get resources for form
        resource_pks = request.session['poet_form_resources']
        resources = Resource.objects.filter(pk__in=resource_pks)
        form = POETSurveyForm()
        form.add_fields_from_resources(resources)
        request.session['poet_form_submitted'] = False
        context['form'] = form
    context['progress_outcomes'] = {x.pk: x for x in ProgressOutcome.objects.exclude(learning_area__exact='')}
    return render(request, template, context)
