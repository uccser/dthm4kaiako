"""Module for admin configuration for the users application."""

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users.forms import UserChangeForm, UserCreationForm
from users.models import Entity, DietaryRequirement
from events.models import EventApplication

User = get_user_model()


class EventApplicationInline(admin.StackedInline):
    """Inline view for event application."""

    model = EventApplication


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """Custom user admin class."""

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['email', 'first_name', 'last_name', 'is_superuser']
    inlines = [EventApplicationInline]


class DietaryRequirementAdmin(admin.ModelAdmin):
    """Admin view for dietary requirements."""

    list_display = (
        'name',
    )


admin.site.register(Entity)
admin.site.register(DietaryRequirement, DietaryRequirementAdmin)
