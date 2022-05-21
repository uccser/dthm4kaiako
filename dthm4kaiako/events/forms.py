"""Forms for events application."""

from django import forms
from events.models import ApplicantType

class EventApplicationForm(forms.Form):
    """ Simple form to allow a user to submit an application to attend an event. """

    applicant_type = forms.ModelChoiceField(ApplicantType.objects)

class TermsAndConditionsForm(forms.Form):
    """ Simple form to allow the user to agree to the terms and conditions.
    This is a different form from the EventRegistrationForm so that the terms 
    and conditions can appear nicely after that form.
    """

    I_agree_to_the_terms_and_conditions = forms.BooleanField(required=True)
