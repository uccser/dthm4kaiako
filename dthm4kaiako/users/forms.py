"""Forms for user application."""

from django.forms import ModelForm
from django.contrib.auth import get_user_model, forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from users.models import Entity, DietaryRequirement
from django.forms import (
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
    CharField,
    EmailField,
    ChoiceField,
    Select,
    Textarea
)
from django.db.models import Q
from crispy_forms.helper import FormHelper
from utils.new_zealand_regions import REGION_CHOICES

User = get_user_model()


class SignupForm(ModelForm):
    """Sign up for user registration."""

    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    class Meta:
        """Metadata for SignupForm class."""

        model = get_user_model()
        fields = ['first_name', 'last_name']

    def signup(self, request, user):
        """Extra logic when a user signs up.

        Required by django-allauth.
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserChangeForm(forms.UserChangeForm):
    """Form class for changing user."""

    class Meta(forms.UserChangeForm.Meta):
        """Metadata for UserChangeForm class."""

        model = User
        fields = ('email', 'last_name')


class UserCreationForm(forms.UserCreationForm):
    """Form class for creating user."""

    class Meta(forms.UserCreationForm.Meta):
        """Metadata for UserCreationForm class."""

        model = User
        fields = ('email', 'first_name', 'last_name')


class UserUpdateDetailsForm(ModelForm):
    """Form class for updating the user's details."""

    user_region = ChoiceField(
        required=True,
        choices=REGION_CHOICES,
        label="Region",
        widget=Select()
    )
    email_address = EmailField(max_length=150, required=True)
    email_address_confirm = EmailField(max_length=150, label="Confirm email address", required=True)
    mobile_phone_number = CharField(max_length=30, required=True)
    mobile_phone_number_confirm = CharField(max_length=30, required=True, label="Confim mobile phone number")
    educational_entities = ModelMultipleChoiceField(
        queryset=Entity.objects.all(),
        required=True,
        widget=CheckboxSelectMultiple,
        label="What school(s) and/or educational organisation or association do you belong to?"
    )

    dietary_requirements = ModelMultipleChoiceField(
        queryset=DietaryRequirement.objects.filter(~Q(name='None')),
        required=False,
        widget=CheckboxSelectMultiple,
        
    )

    how_we_can_best_look_after_you = CharField(
        widget=Textarea(),
        help_text="e.g. accessibility, allergies",
    )

    # TODO: add in for requirmement U38 (ability to add custom dietary requirements)
    # other = CharField(max_length=200, help_text="Any additional dietary requirements", required=False)
    # TODO: change the label for the user_region field to just be "label"

    class Meta:
        """Metadata for UserUpdateDetailsForm class."""

        model = User
        fields = [
            'first_name',
            'last_name',
            'user_region',
            'educational_entities',
        ]

    def __init__(self, *args, **kwargs):
        """Initialise method for user update details form.

        If the dietary requirments multi-check box lists is not desired to be
        visible, 'show_dietary_requirements' in the initial dictionary indicates False.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.fields['how_we_can_best_look_after_you'].widget.attrs['rows'] = 5
        self.fields['dietary_requirements'].help_text = 'We will try out best to cater for you.'

        if 'initial' in kwargs:
            initial_data_dict = kwargs.get('initial')
            if 'show_dietary_requirements' in initial_data_dict:
                self.show_dietary_requirements = initial_data_dict.get('show_dietary_requirements')
                if not self.show_dietary_requirements:
                    del self.fields['dietary_requirements']

            if 'show_medical_notes' in initial_data_dict:
                self.show_medical_notes = initial_data_dict.get('show_medical_notes')
                if not self.show_medical_notes:
                    del self.fields['how_we_can_best_look_after_you']

    def clean(self):
        """Clean the form to check the mobile phone numbers and email addresses match.

        Error is raised is they do not match.
        """
        cleaned_data = super(UserUpdateDetailsForm, self).clean()
        email_address = cleaned_data.get('email_address')
        email_address_confirm = cleaned_data.get('email_address_confirm')
        mobile_phone_number = cleaned_data.get('mobile_phone_number')
        mobile_phone_number_confirm = cleaned_data.get('mobile_phone_number_confirm')

        if email_address and email_address_confirm and email_address != email_address_confirm:
            self._errors['email_address_confirm'] = self.error_class(['Emails do not match.'])
            del self.cleaned_data['email_address_confirm']

        if mobile_phone_number and mobile_phone_number_confirm and mobile_phone_number != mobile_phone_number_confirm:
            self._errors['mobile_phone_number_confirm'] = self.error_class(['Mobile phone numbers do not match.'])
            del self.cleaned_data['mobile_phone_number_confirm']

        return cleaned_data
