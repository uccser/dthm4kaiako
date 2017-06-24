"""Administration configuration for the events application."""

from django.contrib import admin
from events.models import (
    Event,
    ThirdPartyEvent,
    Location,
    Session,
    Sponsor,
    Resource,
)


class SessionAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("name", "event")
    search_fields = ["name", "event"]
    list_filter = ("event",)


class SessionInline(admin.StackedInline):
    model = Session
    extra = 5
    exclude = ("slug",)


class LocationAdmin(admin.ModelAdmin):
    exclude = ("slug",)


class ResourceAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ("name", "url")


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "description"]
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
    list_display = ("name",)
    list_filter = ("is_published",)
    search_fields = ["name"]


class ThirdPartyEventAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "url",
                    "start_date",
                    "end_date",
                    "description",
                    "locations",
                ]
            }
        ),
        (
            "Visibility",
            {
                "fields": ["is_published"]
            }
        ),
    ]
    list_display = ("name",)
    list_filter = ("is_published",)
    search_fields = ["name"]


admin.site.register(Event, EventAdmin)
admin.site.register(ThirdPartyEvent, ThirdPartyEventAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Sponsor)
