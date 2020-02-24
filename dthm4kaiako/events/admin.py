"""Module for admin configuration for the events application."""
import logging
from django.contrib import admin
from django.utils.timezone import now
from django.contrib.gis.db import models as geomodels
from django.utils.translation import gettext_lazy as _
from events.models import (
    Event,
    Session,
    Location,
    Organiser,
    Sponsor,
    Series,
)
from mapwidgets.widgets import GooglePointFieldWidget
from modelclone import ClonableModelAdmin

logger = logging.getLogger(__name__)


class LocationAdmin(admin.ModelAdmin):
    """Inline view for event locations."""

    formfield_overrides = {
        geomodels.PointField: {"widget": GooglePointFieldWidget}
    }
    list_display = (
        'name',
        'room',
        'street_address',
        'suburb',
        'city',
        'region',
    )
    list_filter = ('region', )
    search_fields = (
        'name',
        'room',
        'street_address',
        'suburb',
        'city',
        'region',
    )


class SessionInline(admin.StackedInline):
    """Inline view for event sessions."""

    model = Session
    fk_name = 'event'
    extra = 3
    min_num = 1
    autocomplete_fields = ('locations', )


class EventUpcomingListFilter(admin.SimpleListFilter):
    """Custom filter for events admin."""

    title = _('time')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'time'

    def lookups(self, request, model_admin):
        """Return a list of tuples.

        The first element in each tuple is the coded value for
        the option that will appear in the URL query.
        The second element is the human-readable name for
        the option that will appear in the right sidebar.
        """
        return (
            ('upcoming', _('Upcoming events')),
            ('past', _('Past events')),
            ('all', _('All events')),
        )

    def queryset(self, request, queryset):
        """Return filtered queryset.

        The filtered queryset is based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            self.used_parameters[self.parameter_name] = 'upcoming'
        if self.value() == 'upcoming':
            return queryset.filter(end__gte=now())
        elif self.value() == 'past':
            return queryset.filter(end__lt=now())
        else:
            return queryset

    def choices(self, changelist):
        """Override default method to remove 'All' option."""
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


class EventAdmin(ClonableModelAdmin):
    """Admin view for an event."""

    model = Event
    inlines = [SessionInline]
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'description',
                    'series',
                    'organisers',
                    'sponsors',
                    'price',
                )
            }
        ),
        ('Location', {
            'fields': ('accessible_online', 'locations'),
        }),
        ('Registration', {
            'description': 'Currently only registration via URL is available.',
            'fields': ('registration_link', ),
        }),
        ('Visibility', {
            'fields': (
                'published',
                'featured',
                'show_schedule',
            ),
        }),
    )
    list_display = ('name', 'location_summary', 'series', 'start', 'end', 'published', 'featured')
    list_filter = (EventUpcomingListFilter, 'organisers', )
    ordering = ('start', 'end', 'name')
    autocomplete_fields = ('locations', )
    save_on_top = True

    def save_related(self, request, form, formsets, change):
        """Trigger update of event datetimes after sessions are saved."""
        super().save_related(request, form, formsets, change)
        # Update datetimes on event after saving sessions
        form.instance.update_datetimes()

    class Media:
        """Custom media file overrides."""

        css = {
            'all': ('css/admin-overrides.css', )
        }


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organiser)
admin.site.register(Sponsor)
admin.site.register(Series)
