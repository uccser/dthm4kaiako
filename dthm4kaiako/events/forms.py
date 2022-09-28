"""Forms for events registration."""

from django import forms
from events.models import (
    Address,
    DeletedEventRegistration,
    Event,
    EventRegistration,
    EventRegistrationsCSV,
    EventCSV,
    Location,
    RegistrationForm,
    ParticipantType,
)
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django.forms import EmailField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

User = get_user_model()


# TODO: move into main form?
class ParticipantTypeForm(forms.Form):
    """Simple form to allow a user to select their participant type that is specific to the event."""

    participant_type = forms.ChoiceField(required=True, choices=[], widget=forms.Select())

    def __init__(self, event, *args, **kwargs):
        """Add crispyform helper to form."""
        super(ParticipantTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        choices = [(0, "Select participant type")]
        for participant_type in event.participant_types.all():
            choices += [(participant_type.pk, str(participant_type))]
        self.fields['participant_type'].choices = choices

    def clean(self):
        """Clean participant type so that ones is selected."""
        cleaned_data = super(ParticipantTypeForm, self).clean()
        participant_type = cleaned_data.get('participant_type')

        if participant_type == "0":
            self._errors['participant_type'] = self.error_class(['Must select participant type.'])


class EventRegistrationForm(ModelForm):
    """Simple form to allow a user to submit an registration to attend an event."""

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
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
        """Metadata for EventRegistrationForm class."""

        model = EventRegistration
        fields = [
            'representing',
            'emergency_contact_first_name',
            'emergency_contact_last_name',
            'emergency_contact_relationship',
            'emergency_contact_phone_number',
        ]


class TermsAndConditionsForm(forms.Form):
    """Simple form to allow the user to agree to the terms and conditions.

    This is a different form from the EventRegistrationForm so that the terms
    and conditions can appear nicely after that form.
    """

    I_agree_to_the_terms_and_conditions = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class BillingDetailsForm(ModelForm):
    """Simple form for event registration billing details."""

    bill_to = forms.CharField(max_length=200, required=True, help_text="Who will be paying for you?")
    billing_email_address = EmailField(
        required=True,
        label='Billing email address',
        help_text="Email address of who will be paying for you"
    )

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for BillingDetailsForm class."""

        model = Address
        fields = ['street_number', 'street_name', 'suburb', 'city', 'region', 'post_code', 'country', ]


class WithdrawEventRegistrationForm(ModelForm):
    """Simple form for obtaining the reason for a participant withdrawing from their event registration."""

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for WithdrawEventRegistrationForm class."""

        model = DeletedEventRegistration
        fields = ['withdraw_reason', 'other_reason_for_deletion']


# ---------------------------- Forms for event management ----------------------------------

class ManageEventRegistrationForm(ModelForm):
    """Simple form to allow a user to submit an registration to attend an event."""

    participant_type = forms.ChoiceField(required=True, choices=[], widget=forms.Select())

    def __init__(self, event, *args, **kwargs):
        """Add crispyform helper to form."""
        super(ManageEventRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        choices = [(0, "Select participant type")]
        for participant_type in event.participant_types.all():
            choices += [(participant_type.pk, str(participant_type))]
        self.fields['participant_type'].choices = choices

    def clean(self):
        """Clean participant type so that ones is selected."""
        cleaned_data = super(ManageEventRegistrationForm, self).clean()
        participant_type = cleaned_data.get('participant_type')

        if participant_type == "0":
            self._errors['participant_type'] = self.error_class(['Must select participant type.'])

    class Meta:
        """Metadata for EventRegistrationForm class."""

        model = EventRegistration
        fields = ['status', 'paid', 'staff_comments', 'admin_billing_comments']


class ManageEventDetailsForm(ModelForm):
    """Simple form for managing (e.g. deleting, updating) the information of an event as an event staff member."""

    class Meta:
        """Metadata for ManageEventDetailsForm class."""

        model = Event
        exclude = ('published', 'is_cancelled', 'participant_types')

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super(ManageEventDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ManageEventRegistrationFormDetailsForm(ModelForm):
    """Simple form for updating the event registration form information as an event staff member."""

    class Meta:
        """Metadata for ManageEventRegistrationFormDetailsForm class."""

        model = RegistrationForm
        field = ['open_datetime', 'close_datetime', 'terms_and_conditions']
        exclude = ['event']

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super(ManageEventRegistrationFormDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ManageEventLocationForm(ModelForm):
    """Simple form for updating the event location information as an event staff member."""

    class Meta:
        """Metadata for ManageEventLocationForm class."""

        model = Location
        fields = '__all__'
        exclude = ['event']

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super(ManageEventLocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


# TODO: allow for selecting all boxes at once
# TODO: add multi select for choosing subset of events
class BuilderFormForEventsCSV(ModelForm):
    """Simple form for selecting which Event model fields will be included the generated CSV."""

    class Meta:
        """Metadata for CSVBuilderFormForEvent class."""

        model = EventCSV
        fields = '__all__'
        exclude = ['event']

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super(BuilderFormForEventsCSV, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


# TODO: allow for selecting all boxes at once
# TODO: add multi select for choosing subset of event registrations OR based on type e.g. approved
class BuilderFormForEventRegistrationsCSV(ModelForm):
    """Simple form for selecting which Event Registration model fields will be included the generated CSV."""

    class Meta:
        """Metadata for BuilderFormForEventRegistrationsCSV class."""

        model = EventRegistrationsCSV
        fields = '__all__'
        exclude = ['event']

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super(BuilderFormForEventRegistrationsCSV, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ParticipantTypeCreationForm(ModelForm):
    """Simple form for creating new participant type for an event."""

    class Meta:
        """Metadata for NewParticipantType class."""

        model = ParticipantType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super(ParticipantTypeCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


MESSAGE_TEMPLATE = "{message}\n\n-----\nMessage sent from {user} ({email})"


class ContactParticipantsForm(forms.Form):
    """Form for contacting event participants owners."""

    name = forms.CharField(required=True, label='Your name', max_length=100)
    from_email = forms.EmailField(required=True, label='Email to contact you')
    cc_sender = forms.BooleanField(required=False, label='Send a copy to yourself', initial=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    # TODO: figure out how to get validation for this to work - currently wipes form when invalid
    send_to_approved_participants = forms.BooleanField(
        required=False,
        label='Send to event participants who have been approved'
    )
    # TODO: hide this for events where events are "apply" type (compared to "register" type)
    send_to_pending_applicants = forms.BooleanField(
        required=False,
        label='Send to event applicants who are pending approval'
    )

    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    def __init__(self, *args, **kwargs):
        """Add crispyform helper to form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    def clean(self):
        """Clean the checkboxes for who to send the email to.

        User must select one or both otherwise error messages shows.
        """
        cleaned_data = super(ContactParticipantsForm, self).clean()
        send_to_approved_participants = cleaned_data['send_to_approved_participants']
        send_to_pending_applicants = cleaned_data['send_to_pending_applicants']
        if not send_to_approved_participants and not send_to_pending_applicants:
            self._errors['send_to_approved_participants'] = self.error_class(
                ['Must choose to send email to either or both groups of participants.']
            )
            self._errors['send_to_pending_applicants'] = self.error_class(
                ['Must choose to send email to either or both groups of participants.']
            )


# ------------- Forms for event management when event is cancelled or in the past -------------

PENDING = 1
APPROVED = 2
DECLINED = 3
APPLICATION_STATUSES = (
    (PENDING, _('Pending')),
    (APPROVED, _('Approved')),
    (DECLINED, _('Declined')),
)


class ManageEventRegistrationReadOnlyForm(ModelForm):
    """Simple form to allow a user to submit an registration to attend an event."""

    status = forms.ChoiceField(disabled=True, choices=APPLICATION_STATUSES, required=False)
    paid = forms.BooleanField(disabled=True, required=False)
    staff_comments = forms.CharField(disabled=True, required=False)
    admin_billing_comments = forms.CharField(disabled=True, required=False)

    def __init__(self, *args, **kwargs):
        """Initialise for ManageEventRegistrationFormDetailsForm class.

        Fields are all disabled.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['status'].widget.attrs['disabled'] = True
            self.fields['paid'].widget.attrs['disabled'] = True
            self.fields['staff_comments'].widget.attrs['disabled'] = True
            self.fields['admin_billing_comments'].widget.attrs['disabled'] = True

    class Meta:
        """Metadata for EventRegistrationForm class."""

        model = EventRegistration
        fields = ['status', 'paid', 'staff_comments', 'admin_billing_comments']


class ManageEventDetailsReadOnlyForm(ModelForm):
    """Form for managing (e.g. deleting, updating) the information of an event as an event staff member."""

    class Meta:
        """Metadata for ManageEventDetailsForm class."""

        model = Event
        exclude = ('published', 'is_cancelled', 'participant_types')

    def __init__(self, *args, **kwargs):
        """Initialise for ManageEventRegistrationFormDetailsForm class.

        Fields are all disabled.
        """
        super(ManageEventDetailsReadOnlyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['disabled'] = True
            self.fields['show_schedule'].widget.attrs['disabled'] = True
            self.fields['featured'].widget.attrs['disabled'] = True
            self.fields['registration_type'].widget.attrs['disabled'] = True
            self.fields['external_event_registration_link'].widget.attrs['disabled'] = True
            self.fields['start'].widget.attrs['disabled'] = True
            self.fields['end'].widget.attrs['disabled'] = True
            self.fields['accessible_online'].widget.attrs['disabled'] = True
            self.fields['locations'].widget.attrs['disabled'] = True
            self.fields['sponsors'].widget.attrs['disabled'] = True
            self.fields['organisers'].widget.attrs['disabled'] = True
            self.fields['series'].widget.attrs['disabled'] = True
            self.fields['is_catered'].widget.attrs['disabled'] = True
            self.fields['contact_email_address'].widget.attrs['disabled'] = True
            self.fields['event_staff'].widget.attrs['disabled'] = True


class ManageEventRegistrationFormDetailsReadOnlyForm(ModelForm):
    """Form for updating the event registration form information as an event staff member."""

    class Meta:
        """Metadata for ManageEventRegistrationFormDetailsForm class."""

        model = RegistrationForm
        field = ['open_datetime', 'close_datetime', 'terms_and_conditions']
        exclude = ['event']

    def __init__(self, *args, **kwargs):
        """Initialise for ManageEventRegistrationFormDetailsForm class.

        Fields are all disabled.
        """
        super(ManageEventRegistrationFormDetailsReadOnlyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['open_datetime'].widget.attrs['disabled'] = True
            self.fields['close_datetime'].widget.attrs['disabled'] = True
            self.fields['terms_and_conditions'].widget.attrs['disabled'] = True
