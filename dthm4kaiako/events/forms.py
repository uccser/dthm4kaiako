"""Forms for events application."""

from django import forms
from users.models import User

class AddForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'dietary_requirement': forms.TextInput(attrs={'class': 'form-control'}),
            
            # bootstrap class form-control used
        }