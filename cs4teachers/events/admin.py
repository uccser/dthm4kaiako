"""Administration configuration for the events application."""

from django.contrib import admin
from events.models import (
    Event,
    Session,
    Location,
    Sponsor,
)


class SessionAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("name", "event")
    search_fields = ["name", "event"]
    list_filter = ("event",)


class SessionInline(admin.StackedInline):
    model = Session
    extra = 5


class LocationAdmin(admin.ModelAdmin):
    exclude = ("slug",)


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "description"]
            }
        ),
        (
            "Date information",
            {
                "fields": ["start_date", "end_date"]
            }
        ),
        (
            "Visibility",
            {
                "fields": ["is_published"]
            }
        ),
    ]
    inlines = [SessionInline]
    list_display = ("name", "start_date", "end_date")
    list_filter = ("is_published",)
    search_fields = ["name"]


admin.site.register(Event, EventAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Sponsor)
