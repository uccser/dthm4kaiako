"""Forms for POET application."""

from django import forms

from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
from poet.models import (
    Resource,
    ProgressOutcome,
    ProgressOutcomeGroup,
    Submission,
)
from poet.fields import (
    ResourceField,
    POChoiceField,
    FeedbackField,
)
from poet import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit


class POETSurveySelectorForm(forms.Form):

    po_group = forms.ModelChoiceField(
        queryset=ProgressOutcomeGroup.objects.filter(
            active=True
        ).annotate(
            resource_count=Count(
                'progress_outcomes__resources',
                distinct=True,
                filter=Q(progress_outcomes__resources__active=True)
            )
        ).filter(resource_count__gte=settings.NUM_RESOURCES_PER_FORM),
        empty_label=None,
        label='Select year levels:',
    )

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'po_group',
            Submit('submit', 'Begin survey', css_class="btn-success"),
            HTML('{% if active_survey %}<a class="btn btn-secondary" href={% url "poet:form" %}>Resume incompleted survey</a>{% endif %}'),
        )

class POETSurveyForm(forms.Form):
    """Form for resource displayed in form."""

    def add_fields_from_resources(self, resources):
        """Add fields to form from list of resources."""
        for i, resource in enumerate(resources):
            self.fields['resource' + str(i)] = ResourceField(resource, i + 1)
            self.fields['choice' + str(i)] = POChoiceField(resource)
            self.fields['feedback' + str(i)] = FeedbackField()

    def add_fields_from_request(self, request):
        """Add fields to form from request object."""
        resource_session_pks = request.session.get('poet_form_resources', list())
        if not resource_session_pks:
            raise forms.ValidationError('Resouce IDs not present in session.')
        i = 0
        run_loop = True
        while run_loop:
            resource_pk = int(request.POST['resource' + str(i)])
            if resource_pk != resource_session_pks[i]:
                raise forms.ValidationError('Resource IDs from form do not match session data.')
            choice = request.POST.get('choice' + str(i), None)
            resource = Resource.objects.get(pk=resource_pk)
            self.fields['resource' + str(i)] = ResourceField(
                resource,
                i + 1,
            )
            self.fields['choice' + str(i)] = POChoiceField(
                resource,
                initial=choice,
            )
            self.fields['feedback' + str(i)]=FeedbackField()
            if request.POST.get('resource' + str(i + 1), False):
                i += 1
            else:
                run_loop = False

    def update_form_with_summary(self):
        """Update each choice option with percentage selected."""
        for field_id, field in self.fields.items():
            if field_id.startswith('choice'):
                resource = field.resource
                total_submissions = Submission.objects.filter(resource=resource).count()
                count_data = ProgressOutcome.objects.filter(submissions__resource=resource).values(
                    'code').annotate(count=Count('submissions'))
                percentage_data = dict()
                for data in count_data:
                    percentage_data[data['code']] = (data['count'] / total_submissions)
                field.widget.percentage_data = percentage_data
                field.disabled = True


    def validate(self, request):
        data = []
        i = 0
        run_loop = True
        while run_loop:
            resource_pk = int(request.POST['resource' + str(i)])
            progress_outcome_code = request.POST.get('choice' + str(i), None)
            feedback = request.POST.get('feedback' + str(i), '')

            try:
                resource = Resource.objects.get(pk=resource_pk)
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    'Resource ID %(id)s not found',
                    params={'id': resource_pk},
                )

            if not progress_outcome_code:
                raise forms.ValidationError(
                    'A progress outcome choice is blank, please fill in one option for each table'
                )

            try:
                progress_outcome = ProgressOutcome.objects.get(code=progress_outcome_code)
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    'Progress outcome code %(code)s not found',
                    params={'code': progress_outcome_code},
                )

            data.append({
                'resource': resource,
                'progress_outcome': progress_outcome,
                'feedback': feedback,
            })

            if request.POST.get('resource' + str(i + 1), False):
                i += 1
            else:
                run_loop = False
        return data
