"""Forms for user application."""

# from select import kevent
from django.forms import ModelForm
from django.contrib.auth import get_user_model, forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from users.models import DietaryRequirement
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, EmailField, CharField
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
    """Form class for updating the user's details."""

    from_email = EmailField(required=True, label='Email to contact you')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        # TODO: figure out how to get the dietary requirements to show when either the event is catered or the user is updating their details.
        # Safe to remove this if it is not needed in the update user details form as the event application form contains dietary requirements separately.

        # self.show_dietary_requirements = True
        # if 'initial' in kwargs:
        #     initial_data_dict = kwargs.get('initial')
        #     if 'show_dietary_requirements' in initial_data_dict:
        #         self.show_dietary_requirements = initial_data_dict.get('show_dietary_requirements')

        # if (self.show_dietary_requirements):
        #     dietary_requirements = ModelMultipleChoiceField(queryset=DietaryRequirement.objects.filter(~Q(name='None')), required=False, widget=CheckboxSelectMultiple)
        #     other = CharField(max_length=200, help_text="Any additional dietary requirements", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'school', 'city', 'mobile_phone_number', 'medical_notes',]
