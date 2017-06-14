"""Administration configuration for the events application."""

from django.contrib import admin
from events.models import Event


class EventAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_filter = ('is_published',)

admin.site.register(Event, EventAdmin)
