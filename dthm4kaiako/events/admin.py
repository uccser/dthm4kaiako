"""Module for admin configuration for the events application."""

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


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organiser)
admin.site.register(Sponsor)
admin.site.register(Series)
