"""Forms for user application."""

from django.forms import ModelForm
from django.contrib.auth import get_user_model, forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from users.models import Entity, DietaryRequirement
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, CharField
from django.db.models import Q
from crispy_forms.helper import FormHelper


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
    """
    Form class for updating the user's details.
    """

    educational_entities = ModelMultipleChoiceField(queryset=Entity.objects.all(), required=True, widget=CheckboxSelectMultiple, label="What school(s) and/or educational organisation or association do you belong to?")
    dietary_requirements = ModelMultipleChoiceField(queryset=DietaryRequirement.objects.filter(~Q(name='None')), required=False, widget=CheckboxSelectMultiple)
    
    # TODO: add in for requirmement U38
    # other = CharField(max_length=200, help_text="Any additional dietary requirements", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'region', 'mobile_phone_number', 'educational_entities', 'medical_notes', 'dietary_requirements']

    def __init__(self, *args, **kwargs):
        """
        If the dietary requirments multi-check box lists is not desired to be visible, 'show_dietary_requirements' in the initial dictionary indicates False.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        if 'initial' in kwargs:
            initial_data_dict = kwargs.get('initial')
            if 'show_dietary_requirements' in initial_data_dict:
                self.show_dietary_requirements = initial_data_dict.get('show_dietary_requirements')
                if not self.show_dietary_requirements:
                    del self.fields['dietary_requirements']

            if 'show_medical_notes' in initial_data_dict:
                self.show_medical_notes = initial_data_dict.get('show_medical_notes')
                if not self.show_medical_notes:
                    del self.fields['medical_notes']
