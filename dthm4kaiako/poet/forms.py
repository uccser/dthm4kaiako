"""Forms for POET application."""

from django import forms
from poet.models import ProgressOutcome
from poet.widgets import ProgressOutcomeTableRadioSelect


class POChoiceField(forms.ModelChoiceField):


    def __init__(self, *args, **kwargs):
        super().__init__(
            queryset = ProgressOutcome.objects.order_by('code'),
            to_field_name = 'code',
            required = True,
            empty_label = None,
            initial = ProgressOutcome.objects.filter(code='UNKNOWN').first(),
            widget = ProgressOutcomeTableRadioSelect(),
            label = 'Which progress outcome applies best to this resource:'
        )

    def label_from_instance(self, progress_outcome):
        return progress_outcome.short_label


class Resource1Form(forms.Form):
    choice = POChoiceField()


class Resource2Form(forms.Form):
    choice = POChoiceField()


class Resource3Form(forms.Form):
    choice = POChoiceField()
