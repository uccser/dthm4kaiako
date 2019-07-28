"""Forms for POET application."""

from django import forms
from poet.models import Resource
from poet.fields import (
    ResourceField,
    POChoiceField,
)


class ResourceForm(forms.Form):
    """Form for resource displayed in form."""

    def add_fields_from_resources(self, resources):
        """Add fields to form from list of resources."""
        for i, resource in enumerate(resources):
            self.fields['resource' + str(i)] = ResourceField(resource, i + 1)
            self.fields['choice' + str(i)] = POChoiceField()

    def add_fields_from_request(self, request):
        """Add fields to form from request object."""
        # Get number of resources from session
        resource_session_pks = request.session.get('poet_form_resources', list())
        i = 0
        run_loop = True
        while run_loop:
            resource_pk = int(request.POST['resource' + str(i)])
            choice = request.POST.get('choice' + str(i), None)
            # TODO: Move to field clean method
            if resource_pk != resource_session_pks[i]:
                raise Exception('Resouce PKs do not match')
            resource = Resource.objects.get(pk=resource_pk)
            self.fields['resource' + str(i)] = ResourceField(resource, i + 1)
            self.fields['choice' + str(i)] = POChoiceField(initial=choice)
            if request.POST.get('resource' + str(i + 1), False):
                i += 1
            else:
                run_loop = False
        # Check number matches POST data
        # Check choice exists for each form
