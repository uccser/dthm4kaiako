"""Module for admin configuration for the Ara Ako application."""

import logging
from django.contrib import admin
from ara_ako.models import (
    AraAkoEvent,
    AraAkoTeam,
)

logger = logging.getLogger(__name__)


class AraAkoEventAdmin(admin.ModelAdmin):
    """Admin view for an Ara Ako event."""

    model = AraAkoEvent
    list_display = ('event', 'published', )
    ordering = ('event__start', )
    save_on_top = True


class AraAkoTeamAdmin(admin.ModelAdmin):
    """Admin view for an Ara Ako event."""

    model = AraAkoTeam
    list_display = ('event', 'number', )
    ordering = ('event__start', 'number', )
    save_on_top = True


admin.site.register(AraAkoEvent, AraAkoEventAdmin)
admin.site.register(AraAkoTeam, AraAkoTeamAdmin)
