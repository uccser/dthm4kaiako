"""Module for admin configuration for the users application."""

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users.forms import UserChangeForm, UserCreationForm
from users.models import Entity
from events.models import EventApplication

User = get_user_model()


class EventApplicationInline(admin.StackedInline):
    """Inline view for event registration form."""

    model = EventApplication


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """Custom user admin class."""

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['email', 'first_name', 'last_name', 'is_superuser']
    inlines = [EventApplicationInline]


admin.site.register(Entity)
