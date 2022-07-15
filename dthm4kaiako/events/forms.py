"""Forms for events application."""

# from attr import fields
from django import forms
from events.models import ApplicantType, Address
from users.models import DietaryRequirement
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, EmailField, CharField
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class EventApplicationForm(forms.Form):
    """ Simple form to allow a user to submit an application to attend an event. """

    participant_email_address = EmailField(required=True, label='Email to contact you')
    applicant_type = forms.ModelChoiceField(ApplicantType.objects)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


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

    billing_email_address = EmailField(required=True, label='Billing email address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        """Metadata for BillingDetailsForm class."""

        model = Address
        fields = ['street_number', 'street_name', 'suburb', 'city', 'region', 'post_code', 'country']


class DietaryRequirementsForm(forms.Form):
    """Form class for event registration billing details."""

    # TODO: add this back once implemented associated funcitonality for creating custom DRs that only that user sees
    # other = CharField(max_length=200, help_text="We will do our best to cater for any additional dietary requirements. If your needs are more specific, please bring your own food.", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        # if 'initial' in kwargs:
        #     initial_data_dict = kwargs.get('initial')
        #     if 'show_dietary_requirements' in initial_data_dict:
        #         self.show_dietary_requirements = initial_data_dict.get('show_dietary_requirements')
        #         self.dietary_requirements = ModelMultipleChoiceField(queryset=DietaryRequirement.objects.filter(~Q(name='None')), required=False, widget=CheckboxSelectMultiple)


    class Meta:
        model = DietaryRequirement