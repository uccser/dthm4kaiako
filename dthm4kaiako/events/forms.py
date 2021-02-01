"""Forms for events application."""

from django.forms import ModelForm
# from django.contrib.auth import get_user_model
from events.models import RegistrationForm

# User = get_user_model()


class EventRegistrationForm(ModelForm):
    """Form for a user to register for an event."""

    class Meta:
        model = RegistrationForm
        fields = [
            'terms_and_conditions',
            'event',
        ]
