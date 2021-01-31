"""Forms for events application."""

from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()


class EventRegistrationForm(ModelForm):
    """Form for a user to register for an event."""

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'workplace',
            'city',
            'cell_phone_number',
            'medical_notes',
            'event_applications',
            'billing_address',
        ]
