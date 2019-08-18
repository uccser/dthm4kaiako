"""Views for POET application."""

from ipware import get_client_ip
from json import dumps
from django.forms import ValidationError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
)
from django.views.generic.edit import FormView
from poet.forms import (
    POETSurveySelectorForm,
    POETSurveyForm,
    POETContactForm,
)
from poet.models import (
    Submission,
    ProgressOutcome,
    Resource,
)
from poet.utils import select_resources_for_poet_form
from poet import settings as poet_settings


class HomeView(FormView):
    """View for POET homepage."""

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
        except (ObjectDoesNotExist, ValidationError):
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
    context['progress_outcomes'] = ProgressOutcome.objects.exclude(learning_area__exact='')
    context['progress_outcomes_json'] = dumps(list(ProgressOutcome.objects.values()))
    return render(request, template, context)


class StatisticsListView(PermissionRequiredMixin, ListView):
    """View for POET statistics list page."""

    model = ProgressOutcome
    context_object_name = 'resources'
    template_name = 'poet/statistics.html'
    permission_required = 'poet.view_submission'

    def get_queryset(self):
        """Get queryset for page.

        Returns:
        Progress outcomes with resources.
        """
        return Resource.objects.all().order_by(
            'target_progress_outcome',
            'title',
        ).annotate(submission_count=Count('submissions')).prefetch_related(
            'submissions',
            'target_progress_outcome',
        )

    def get_context_data(self, **kwargs):
        """Provide the context data for the event homepage view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        for resource in self.object_list:
            if resource.submission_count > 0:
                # Add top 3 selected progress outcomes
                # TODO: Perform as one query, possibly when requesting queryset
                resource.crowdsourced_pos = ProgressOutcome.objects.filter(
                    submissions__resource=resource
                ).annotate(
                    submission_count=Count('submissions')
                ).order_by('-submission_count')[:3]
                total_submission_count = Submission.objects.filter(resource=resource).count()
                for crowdsourced_po in resource.crowdsourced_pos:
                    crowdsourced_po.percentage = (crowdsourced_po.submission_count / total_submission_count) * 100
                    if resource.target_progress_outcome != crowdsourced_po:
                        crowdsourced_po.resource_target = True
        context['total_submissions'] = Submission.objects.count()
        context['submission_threshold'] = poet_settings.MINIMUM_SUBMISSIONS_PER_RESOURCE
        return context


class StatisticsDetailsView(PermissionRequiredMixin, DetailView):
    """View for POET statistics details page."""

    model = Resource
    context_object_name = 'resource'
    template_name = 'poet/statistics_detail.html'
    permission_required = 'poet.view_submission'

    def get_context_data(self, **kwargs):
        """Provide the context data for the event homepage view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['statistics'] = True
        total_submissions = Submission.objects.filter(resource=self.object).count()
        progress_outcomes = {x.code: x for x in ProgressOutcome.objects.annotate(
            count=Count('submissions', filter=Q(submissions__resource=self.object)))}
        for progress_outcome_code, progress_outcome in progress_outcomes.items():
            if total_submissions:
                progress_outcome.percentage = progress_outcome.count / total_submissions
            else:
                progress_outcome.percentage = 0
        context['total_submissions'] = total_submissions
        context['progress_outcomes'] = progress_outcomes
        context['progress_outcome_widget'] = 'poet/widgets/progress-outcome-radio-statistics.html'
        context['feedback_submissions'] = self.object.submissions.exclude(feedback__exact='')
        return context


class AboutView(TemplateView):
    """View for website about page."""

    template_name = 'poet/about.html'


class ContactView(FormView):
    """View for website contact page."""

    template_name = 'poet/contact.html'
    form_class = POETContactForm

    def form_valid(self, form):
        """Send email if form is valid."""
        form.send_email()
        messages.success(self.request, 'Your email has been sent.')
        return redirect(reverse('poet:home'))
