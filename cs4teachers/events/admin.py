"""Administration configuration for the events application."""

from django.contrib import admin
from events.models import (
    Event,
    Session,
    Location,
    Sponsor,
)


class EventAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_filter = ('is_published',)


class SessionAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class LocationAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(Event, EventAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Sponsor)
