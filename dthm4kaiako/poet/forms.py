"""Forms for POET application."""

from django import forms
from poet.fields import (
    ResourceField,
    POChoiceField,
)


class ResourceForm(forms.Form):
    """Form for resource displayed in form."""

    def add_resources(self, resources):
        """Add resources for form."""
        for i, resource in enumerate(resources):
            self.fields['resource' + str(i)] = ResourceField(resource)
            self.fields['choice' + str(i)] = POChoiceField()
