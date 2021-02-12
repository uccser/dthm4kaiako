"""Forms for user application."""

from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.contrib.auth import get_user_model, forms
from users.models import DietaryRequirement

User = get_user_model()


class SignupForm(ModelForm):
    """Sign up for user registration."""

    dietary_requirements = ModelMultipleChoiceField(
        queryset=DietaryRequirement.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        """Metadata for SignupForm class."""

        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'workplace',
            'city',
            'cell_phone_number',
            'dietary_requirements',
            'medical_notes',
            'billing_address',
        )

    def signup(self, request, user):
        """Extra logic when a user signs up.

        Required by django-allauth.
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.workplace = self.cleaned_data['workplace']
        user.city = self.cleaned_data['city']
        user.cell_phone_number = self.cleaned_data['cell_phone_number']
        user.dietary_requirements = self.cleaned_data['dietary_requirements']
        user.medical_notes = self.cleaned_data['medical_notes']
        user.billing_address = self.cleaned_data['billing_address']
        user.save()


class UserChangeForm(forms.UserChangeForm):
    """Form class for changing user."""

    dietary_requirements = ModelMultipleChoiceField(
        queryset=DietaryRequirement.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta(forms.UserChangeForm.Meta):
        """Metadata for UserChangeForm class."""

        model = User
        fields = (
            'first_name',
            'last_name',
            'workplace',
            'city',
            'cell_phone_number',
            'dietary_requirements',
            'medical_notes',
            'billing_address',
        )


class UserCreationForm(forms.UserCreationForm):
    """Form class for creating user."""

    dietary_requirements = ModelMultipleChoiceField(
        queryset=DietaryRequirement.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta(forms.UserCreationForm.Meta):
        """Metadata for UserCreationForm class."""

        model = User
        fields = (
            'first_name',
            'last_name',
            'workplace',
            'city',
            'cell_phone_number',
            'dietary_requirements',
            'medical_notes',
            'billing_address',
        )


class UserUpdateForm(ModelForm):
    """Form class for updating user details."""

    dietary_requirements = ModelMultipleChoiceField(
        queryset=DietaryRequirement.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta(forms.UserCreationForm.Meta):
        """Metadata for UserUpdateForm class."""

        model = User
        fields = (
            'first_name',
            'last_name',
            'workplace',
            'city',
            'cell_phone_number',
            'dietary_requirements',
            'medical_notes',
            'billing_address',
        )
