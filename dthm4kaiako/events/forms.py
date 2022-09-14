"""Forms for events application."""

# from attr import fields
from dataclasses import field
from decimal import MAX_EMAX
from email.policy import default
from django import forms
from events.models import (Address, 
                           DeletedEventApplication, 
                           EventApplication, 
                           Event, 
                           RegistrationForm,
                           Location,
                           EventCSV,
                           EventApplicationsCSV, Ticket,
                           )
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django.forms import EmailField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
User = get_user_model()

class ParticipantTypeForm(forms.Form):
    """ Simple form to allow a user to select their ticket/participant type that is specific to the event. """

    participant_type = forms.ChoiceField(required=True, choices=[], widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(ParticipantTypeForm, self).__init__(*args, **kwargs) 
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        ticket_types = self.initial['ticket_types']
        choices = [(0, "Select participant type")]
        choices = [(ticket.pk, ticket.toString()) for ticket in ticket_types]
        self.fields['participant_type'].choices = choices

    # TODO: test this
    # def clean(self):
    #     cleaned_data = super(ParticipantTypeForm, self).clean()
    #     participant_type = cleaned_data.get('participant_type')

    #     if participant_type == "0":
    #         self._errors['participant_type'] = self.error_class(['Must select participant type.'])


class EventApplicationForm(ModelForm):
    """ Simple form to allow a user to submit an application to attend an event. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        # TODO: figure out how to make emergency details not visible nor mandatory in online event registration forms
        # if 'initial' in kwargs:
        #     initial_data_dict = kwargs.get('initial')
        #     if 'show_emergency_contact_fields' in initial_data_dict:
        #         self.show_emergency_contact_fields = initial_data_dict.get('show_emergency_contact_fields')
        #         if not self.show_emergency_contact_fields:
        #             del self.fields['emergency_contact_first_name']
        #             del self.fields['emergency_contact_last_name']
        #             del self.fields['emergency_contact_relationship']
        #             del self.fields['emergency_contact_phone_number']


    class Meta:
        """Metadata for EventApplicationForm class."""

        model = EventApplication
        fields = ['representing', 'emergency_contact_first_name',
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


# ---------------------------- Forms for event management ----------------------------------

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
        fields = ['status', 'paid', 'participant_type', 'staff_comments', 'admin_billing_comments']

class ManageEventDetailsForm(ModelForm):
    """ Simple form for managing (e.g. deleting, updating) the information of an event as an event staff member."""

    class Meta:
        """Metadata for ManageEventDetailsForm class."""

        model = Event
        exclude = ('published', 'is_cancelled', 'ticket_types')
    
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

# TODO: allow for selecting all boxes at once
# TODO: add multi select for choosing subset of events
class BuilderFormForEventsCSV(ModelForm):
    """ Simple form for selecting which Event model fields will be included the generated CSV."""

    class Meta:
        """Metadata for CSVBuilderFormForEvent class."""

        model = EventCSV
        fields = '__all__'
        exclude = ['event']
        
    def __init__(self, *args, **kwargs):
        super(BuilderFormForEventsCSV, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


# TODO: allow for selecting all boxes at once
# TODO: add multi select for choosing subset of event applications OR based on type e.g. approved
class BuilderFormForEventApplicationsCSV(ModelForm):
    """ Simple form for selecting which Event Application model fields will be included the generated CSV."""

    class Meta:
        """Metadata for BuilderFormForEventApplicationsCSV class."""

        model = EventApplicationsCSV
        fields = '__all__'
        exclude = ['event']
        
    def __init__(self, *args, **kwargs):
        super(BuilderFormForEventApplicationsCSV, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class TicketTypeForm(ModelForm):
    """ Simple form for creating new ticket/participant type for an event."""

    class Meta:
        """Metadata for NewTicketType class."""

        model = Ticket
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(TicketTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        
MESSAGE_TEMPLATE = "{message}\n\n-----\nMessage sent from {user} ({email})"


class ContactParticipantsForm(forms.Form):
    """Form for contacting event participants owners."""

    name = forms.CharField(required=True, label='Your name', max_length=100)
    from_email = forms.EmailField(required=True, label='Email to contact event participants')
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    #TODO: figure out how to get validation for this to work - currently wipes form when invalid
    send_to_approved_participants = forms.BooleanField(required=False, label='Send to event participants who have been approved')
    send_to_pending_applicants = forms.BooleanField(required=False, label='Send to event applicants who are pending approval') #TODO: hide this for events where events are "apply" type (compared to "register" type)
    
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
    
    # TODO: figure out how to get this to show
    def clean(self):
        cleaned_data = super(ContactParticipantsForm, self).clean()
        send_to_approved_participants = cleaned_data.get('send_to_approved_participants')
        send_to_pending_applicants = cleaned_data.get('send_to_pending_applicants')
        if send_to_approved_participants == False and send_to_pending_applicants == False:
            self._errors['send_to_approved_participants'] = self.error_class(['Must choose to send email to either or both groups of participants.'])


# ---------------------------- Forms for event management when event is cancelled or in the past ----------------------------------

PENDING = 1
APPROVED = 2
REJECTED = 3
APPLICATION_STATUSES = (
    (PENDING, _('Pending')),
    (APPROVED, _('Approved')),
    (REJECTED, _('Rejected')),
)

class ManageEventApplicationReadOnlyForm(ModelForm):
    """ Simple form to allow a user to submit an application to attend an event. """

    status = forms.ChoiceField(disabled = True, choices = APPLICATION_STATUSES, required=False)
    paid = forms.BooleanField(disabled = True, required=False)
    staff_comments = forms.CharField(disabled=True, required=False)
    admin_billing_comments = forms.CharField(disabled = True, required=False)

    #TODO: ticket type

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for EventApplicationForm class."""
        model = EventApplication
        exclude = ['submitted', 'updated', 'status', 'staff_comments', 'participant_type',
        'staff_comments', 'user', 'representing', 'event', 'emergency_contact_first_name',
        'emergency_contact_last_name', 'emergency_contact_relationship', 'emergency_contact_phone_number',
        'paid', 'bill_to', 'billing_physical_address', 'billing_email_address', 'admin_billing_comments']


class ManageEventDetailsReadOnlyForm(ModelForm):
    """ Simple form for managing (e.g. deleting, updating) the information of an event as an event staff member."""

    class Meta:
        """Metadata for ManageEventDetailsForm class."""

        model = Event
        exclude = ('published', 'is_cancelled', 'ticket_types')
    
    def __init__(self, *args, **kwargs):
        super(ManageEventDetailsReadOnlyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['show_schedule'].widget.attrs['readonly'] = True
            self.fields['featured'].widget.attrs['readonly'] = True
            self.fields['registration_type'].widget.attrs['readonly'] = True
            self.fields['registration_link'].widget.attrs['readonly'] = True
            self.fields['start'].widget.attrs['readonly'] = True
            self.fields['end'].widget.attrs['readonly'] = True
            self.fields['accessible_online'].widget.attrs['readonly'] = True
            self.fields['locations'].widget.attrs['readonly'] = True
            self.fields['sponsors'].widget.attrs['readonly'] = True
            self.fields['organisers'].widget.attrs['readonly'] = True
            self.fields['series'].widget.attrs['readonly'] = True
            self.fields['is_catered'].widget.attrs['readonly'] = True
            self.fields['contact_email_address'].widget.attrs['readonly'] = True
            self.fields['event_staff'].widget.attrs['readonly'] = True


class ManageEventRegistrationFormDetailsReadOnlyForm(ModelForm):
    """ Simple form for updating the event registration form information as an event staff member."""

    class Meta:
        """Metadata for ManageEventRegistrationFormDetailsForm class."""

        model = RegistrationForm
        field = ['open_datetime', 'close_datetime', 'terms_and_conditions']
        exclude = ['event']        
    
    def __init__(self, *args, **kwargs):
        super(ManageEventRegistrationFormDetailsReadOnlyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['open_datetime'].widget.attrs['readonly'] = True
            self.fields['close_datetime'].widget.attrs['readonly'] = True
            self.fields['terms_and_conditions'].widget.attrs['readonly'] = True

