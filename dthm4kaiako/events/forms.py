"""Forms for events application."""

# from attr import fields
from dataclasses import field
from django import forms
from pkg_resources import require
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
from users.models import Entity, DietaryRequirement
from django.db.models import Q
from .widgets import DateTimePickerInput

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


# Playing around with trying to get non-disabled fields to show initial data
# class ManageEventApplicationForm(forms.Form):
#     """ Simple form for managing (e.g. deleting, updating) the information in an event application as an event staff member."""

#     staff_comments = forms.CharField(required=False)
#     participant_first_name = forms.CharField(disabled=True, max_length=50, label='participant first name')

    # def __init__(self, *args, **kwargs):
    #     super(ManageEventApplicationForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_tag = False
    #     self.helper.disable_csrf = True

        # self.fields['representing'].disabled = True
        # self.fields['emergency_contact_first_name'].disabled = True
        # self.fields['emergency_contact_last_name'].disabled = True
        # self.fields['emergency_contact_relationship'].disabled = True
        # self.fields['emergency_contact_phone_number'].disabled = True
        # self.fields['bill_to'].disabled = True
        # self.fields['billing_physical_address'].disabled = True
        # self.fields['billing_email_address'].disabled = True


    # class Meta:
    #     """Metadata for EventApplicationForm class."""

    #     model = EventApplication
    #     fields = ['staff_comments', 'paid', 'participant_type', 'representing', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_relationship',
    #                 'emergency_contact_phone_number', 'bill_to', 'billing_physical_address', 'billing_email_address'
    #                 ]

# TODO: add submitted and updated fields (read only by default) 
# TODO: check that the disabled fields fall back correctly the default provided in "initial"
# class ManageEventApplicationForm(ModelForm):
#     """ Simple form for managing (e.g. deleting, updating) the information in an event application as an event staff member."""

#     participant_first_name = forms.CharField(disabled=True, max_length=50, label='participant first name')
#     participant_last_name = forms.CharField(disabled=True, max_length=50, label='participant last name')
#     participant_region_name = forms.CharField(disabled=True)
#     # educational_entities = forms.ModelMultipleChoiceField(disabled=True, queryset=Entity.objects.all(), required=True, widget=forms.CheckboxSelectMultiple, label="What school(s) and/or educational organisation or association do you belong to?")
#     dietary_requirements = forms.ModelMultipleChoiceField(disabled=True, queryset=DietaryRequirement.objects.filter(~Q(name='None')), required=False, widget=forms.CheckboxSelectMultiple)
#     medical_notes = forms.CharField(disabled=True)
#     email_address = forms.EmailField(disabled=True, max_length=150)
#     mobile_phone_number = forms.CharField(disabled=True, max_length=30)
#     submitted = forms.DateTimeField(disabled=True)
#     updated = forms.DateTimeField(disabled=True)
#     staff_comments = forms.CharField(required=False)

#     class Meta:
#         """Metadata for ManageEventApplicationForm class."""

#         model = Event
#         fields = '__all__'

#         #TODO: add in status
#         model = EventApplication
#         fields = ['participant_type', 'representing',
#                     'event', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_relationship',
#                     'emergency_contact_phone_number', 'paid', 'bill_to', 'billing_physical_address', 'billing_email_address'
#                     ]
        
    
#     def __init__(self, *args, **kwargs):
#         super(ManageEventApplicationForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_tag = False
#         self.helper.disable_csrf = True

#         self.fields['representing'].disabled = True
#         self.fields['event'].disabled = True
#         self.fields['emergency_contact_first_name'].disabled = True
#         self.fields['emergency_contact_last_name'].disabled = True
#         self.fields['emergency_contact_relationship'].disabled = True
#         self.fields['emergency_contact_phone_number'].disabled = True
#         self.fields['bill_to'].disabled = True
#         self.fields['billing_physical_address'].disabled = True
#         self.fields['billing_email_address'].disabled = True


class ManageEventDetailsForm(ModelForm):
    """ Simple form for managing (e.g. deleting, updating) the information of an event as an event staff member."""

    class Meta:
        """Metadata for ManageEventDetailsForm class."""

        model = Event
        fields = '__all__'
        
    
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
        