"""Forms for events application."""

# from attr import fields
from django import forms
from pkg_resources import require
from events.models import Address, DeletedEventApplication, EventApplication
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django.forms import EmailField
from django.contrib.auth import get_user_model

User = get_user_model()

class EventApplicationForm(ModelForm):
    """ Simple form to allow a user to submit an application to attend an event. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        if 'initial' in kwargs:
            initial_data_dict = kwargs.get('initial')
            if 'show_emergency_contact_fields' in initial_data_dict:
                self.show_emergency_contact_fields = initial_data_dict.get('show_emergency_contact_fields')
                if not self.show_emergency_contact_fields:
                    del self.fields['emergency_contact_first_name']
                    del self.fields['emergency_contact_last_name']
                    del self.fields['emergency_contact_relationship']
                    del self.fields['emergency_contact_phone_number']


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
    """Simple form for event registration billing details."""

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


class WithdrawEventApplicationForm(ModelForm):
    """Simple form for obtaining the reason for a participant withdrawing from their event application."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for WithdrawEventApplicationForm class."""

        model = DeletedEventApplication
        fields = ['deletion_reason', 'other_reason_for_deletion']