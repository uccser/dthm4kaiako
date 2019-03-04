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
        ('Timings', {
            'description': 'Will be overridden if any sessions are provided.',
            'fields': (
                'start',
                'end'
            ),
        }),
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
        event = form.instance

        if event.sessions.all().exists():
            print('Exists')
            logger.info('Event sessions detected for {} so setting event times based off sessions.'.format(event))
            event.start = event.sessions.order_by('start').first().start
            event.end = event.sessions.order_by('-end').first().end
            event.save()


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organiser)
admin.site.register(Sponsor)
admin.site.register(Series)
