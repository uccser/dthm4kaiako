"""Forms for events application."""

# from attr import fields
from dataclasses import field
from django import forms
from events.models import (Address, 
                           DeletedEventApplication, 
                           EventApplication, 
                           Event, 
                           RegistrationForm,
                           Location)
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django.forms import EmailField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

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
        fields = ['participant_type', 'representing', 'emergency_contact_first_name',
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

# ---------------------------- forms for event management ----------------------------------

class ManageEventApplicationForm(ModelForm):
    """ Simple form to allow a user to submit an application to attend an event. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for EventApplicationForm class."""

        model = EventApplication
        fields = ['paid', 'participant_type', 'staff_comments', 'admin_billing_comments']

class ManageEventDetailsForm(ModelForm):
    """ Simple form for managing (e.g. deleting, updating) the information of an event as an event staff member."""

    class Meta:
        """Metadata for ManageEventDetailsForm class."""

        model = Event
        exclude = ('published',)
    
    def __init__(self, *args, **kwargs):
        super(ManageEventDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class DateTimePickerInput(forms.DateTimeInput):
        input_type = 'datetime'


class ManageEventRegistrationFormDetailsForm(ModelForm):
    """ Simple form for updating the event registration form information as an event staff member."""

    class Meta:
        """Metadata for ManageEventRegistrationFormDetailsForm class."""

        model = RegistrationForm
        field = ['open_datetime', 'close_datetime', 'terms_and_conditions']
        exclude = ['event']        
    
    def __init__(self, *args, **kwargs):
        super(ManageEventRegistrationFormDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ManageEventLocationForm(ModelForm):
    """ Simple form for updating the event location information as an event staff member."""

    class Meta:
        """Metadata for ManageEventLocationForm class."""

        model = Location
        fields = '__all__'
        exclude = ['event']
        
    
    def __init__(self, *args, **kwargs):
        super(ManageEventLocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        