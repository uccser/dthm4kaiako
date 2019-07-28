"""Fields for forms in POET application."""

from django import forms
from poet.models import ProgressOutcome
from poet.widgets import (
    ResourcePDFPreviewWithPK,
    ProgressOutcomeTableRadioSelect,
)


class ResourceField(forms.IntegerField):
    """Field for resource in POET form.

    - PDF is shown in viewer.
    - Value is disabled (used to track PO choice against resource)
    """

    def __init__(self, resource, number, *args, **kwargs):
        """Initialise method."""
        super().__init__(
            required=True,
            initial=resource.pk,
            label='',
            widget=ResourcePDFPreviewWithPK(resource, number),
        )


class POChoiceField(forms.ModelChoiceField):
    """Field for PO choices displayed in form.

    - Field widget is custom HTML table.
    """

    def __init__(self, *args, **kwargs):
        """Initialise method."""
        super().__init__(
            queryset=ProgressOutcome.objects.order_by('code'),
            to_field_name='code',
            required=True,
            initial=kwargs.get('initial'),
            empty_label=None,
            widget=ProgressOutcomeTableRadioSelect(),
            label='Which progress outcome applies best to this resource:'
        )

    def label_from_instance(self, progress_outcome):
        """Return label for each progress outcome."""
        return progress_outcome.short_label
