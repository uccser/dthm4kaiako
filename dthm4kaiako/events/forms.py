"""Forms for events application."""

from django import forms
from events.models import ApplicantType, Address
from django.forms import ModelForm


class EventApplicationForm(forms.Form):
    """ Simple form to allow a user to submit an application to attend an event. """

    applicant_type = forms.ModelChoiceField(ApplicantType.objects)


class TermsAndConditionsForm(forms.Form):
    """ Simple form to allow the user to agree to the terms and conditions.
    This is a different form from the EventRegistrationForm so that the terms 
    and conditions can appear nicely after that form.
    """

    I_agree_to_the_terms_and_conditions = forms.BooleanField(required=True)


class BillingDetailsForm(ModelForm):
    """Form class for event registration billing details."""


    class Meta:
        """Metadata for BillingDetailsForm class."""

        model = Address
        fields = ['street_number', 'street_name', 'suburb', 'city', 'region', 'post_code', 'country']
