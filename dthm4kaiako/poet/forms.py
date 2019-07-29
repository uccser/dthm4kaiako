"""Forms for POET application."""

from django import forms
from django.db.models import Count
from poet.models import (
    Resource,
    ProgressOutcome,
    Submission,
)
from poet.fields import (
    ResourceField,
    POChoiceField,
    FeedbackField,
)


class ResourceForm(forms.Form):
    """Form for resource displayed in form."""

    def add_fields_from_resources(self, resources):
        """Add fields to form from list of resources."""
        for i, resource in enumerate(resources):
            self.fields['resource' + str(i)] = ResourceField(resource, i + 1)
            self.fields['choice' + str(i)] = POChoiceField(resource)
            self.fields['feedback' + str(i)] = FeedbackField()

    def add_fields_from_request(self, request):
        """Add fields to form from request object."""
        # Get number of resources from session
        # Check number matches POST data
        # Check choice exists for each form
        resource_session_pks = request.session.get('poet_form_resources', list())
        i = 0
        run_loop = True
        while run_loop:
            resource_pk = int(request.POST['resource' + str(i)])
            choice = request.POST.get('choice' + str(i), None)
            # TODO: Move to field clean method
            if not resource_session_pks or resource_pk != resource_session_pks[i]:
                raise Exception('Resouce PKs do not match')
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
