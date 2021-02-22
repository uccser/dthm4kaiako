"""Forms for events application."""

from django import forms
from events.models import ApplicantType


class EventRegistrationForm(forms.Form):
    """Form for a user to register for an event."""

    applicant_type = forms.ModelChoiceField(ApplicantType.objects.none())
    voucher = forms.CharField(required=False)


class TermsAndConditionsForm(forms.Form):
    """Form for accepting terms and conditions.

    This is separate from EventRegistrationForm so we can render T's & C's at the end of the form.
    """

    terms_and_conditions_accepted = forms.BooleanField(required=True)
