"""Forms for events application."""

# from attr import fields
from django import forms
from pkg_resources import require
from events.models import ParticipantType, Address, EventApplication
from users.models import DietaryRequirement
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, EmailField, CharField
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class EventApplicationForm(ModelForm):
    """ Simple form to allow a user to submit an application to attend an event. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for EventApplicationForm class."""

        model = EventApplication
        fields = ['participant_type', 'emergency_contact_first_name',
                  'emergency_contact_last_name', 'emergency_contact_relationship', 'emergency_contact_phone_number'
                 ]
   

class TermsAndConditionsForm(forms.Form):
    """ Simple form to allow the user to agree to the terms and conditions.
    This is a different form from the EventRegistrationForm so that the terms
    and conditions can appear nicely after that form.
    """

    I_agree_to_the_terms_and_conditions = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class BillingDetailsForm(ModelForm):
    """Form class for event registration billing details."""

    bill_to = forms.CharField(max_length=200, required=True, help_text="Who will be paying for you?")
    billing_email_address = EmailField(required=True, label='Billing email address', help_text="Email address of who will be paying for you")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for BillingDetailsForm class."""

        model = Address
        fields = ['street_number', 'street_name', 'suburb', 'city', 'region', 'post_code', 'country', ]
