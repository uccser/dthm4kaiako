"""Forms for events application."""

from django import forms
from events.models import ApplicantType

class EventApplicationForm(forms.Form):
    """ Simple form to allow a user to submit an application to attend an event. """

    applicant_type = forms.ModelChoiceField(ApplicantType.objects.none())

class TermsAndConditionsForm(forms.Form):
    """ Simple form to allow the user to agree to the terms and conditions.
    This is a different form from the EventRegistrationForm so that the terms 
    and conditions can appear nicely after that form.
    """

    has_agreed = forms.BooleanField(required=True)

