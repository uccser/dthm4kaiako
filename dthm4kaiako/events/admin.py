"""Module for admin configuration for the events application."""
import logging
from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from events.models import (
    Event,
    Session,
    Location,
    Organiser,
    Sponsor,
    Series,
)
from mapwidgets.widgets import GooglePointFieldWidget

logger = logging.getLogger(__name__)


class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }


class SessionInline(admin.StackedInline):
    """Inline view for event sessions."""

    model = Session
    fk_name = 'event'
    extra = 1
    min_num = 1


class EventAdmin(admin.ModelAdmin):
    """Admin view for an event."""

    model = Event
    inlines = [SessionInline]
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'locations',
                'series',
                'organisers',
                'sponsors',
            )}
        ),
        ('Registration', {
            'description': 'Currently only registration via URL is available.',
            'fields': ('registration_link', ),
        }),
        ('Visibility', {
            'fields': ('published', ),
        }),
    )
    list_display = ('name', 'start', 'end')
    ordering = ('start', 'end', 'name')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Update datetimes on event after saving sessions
        form.instance.update_datetimes()


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organiser)
admin.site.register(Sponsor)
admin.site.register(Series)
