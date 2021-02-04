"""Forms for events application."""

from django import forms


class EventRegistrationForm(forms.Form):
    """Form for a user to register for an event."""

    terms_and_conditions_accepted = forms.BooleanField(required=True)
