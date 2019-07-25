"""Forms for POET application."""

from django import forms
from poet.models import ProgressOutcome
from poet.widgets import ProgressOutcomeTableRadioSelect


class Resource1Form(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=ProgressOutcome.objects.all(),
        to_field_name='code',
        required=True,
        initial='UNKNOWN',
        widget=ProgressOutcomeTableRadioSelect(),
        label='Which progress outcome applies best to this resource:'
    )


class Resource2Form(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=ProgressOutcome.objects.all(),
        to_field_name='code',
        required=True,
        widget=ProgressOutcomeTableRadioSelect(),
        label='Which progress outcome applies best to this resource:'
    )


class Resource3Form(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=ProgressOutcome.objects.all(),
        to_field_name='code',
        required=True,
        widget=ProgressOutcomeTableRadioSelect(),
        label='Which progress outcome applies best to this resource:'
    )
