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
    Series,
    EventApplication,
    RegistrationForm,
    ApplicantType,
)
from mapwidgets.widgets import GooglePointFieldWidget
from modelclone import ClonableModelAdmin
from users.models import User
from django.utils.html import format_html_join

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
    ordering = ('start', 'end', 'name')
    autocomplete_fields = ('locations', )


class RegistrationFormInline(admin.StackedInline):
    """Inline view for event registration form."""

    model = RegistrationForm
    fk_name = 'event'
    extra = 0
    min_num = 1


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
    inlines = [SessionInline, RegistrationFormInline]
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
                    'is_catered',
                )
            }
        ),
        ('Location', {
            'fields': ('accessible_online', 'locations'),
        }),
        ('Registration', {
            'description': 'Currently only registration via URL is available.',
            'fields': (
                'registration_link',
                'registration_type',
            ),
        }),
        ('Visibility', {
            'fields': (
                'published',
                'featured',
                'show_schedule',
            ),
        }),
    )
    filter_horizontal = (
        'organisers',
        'sponsors',
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



class EventApplicationAdmin(admin.ModelAdmin):
    """Admin view for an event application."""

    model = EventApplication
    readonly_fields = [
        'user',
        'user_school',
        'user_city',
        'user_dietary_requirements',
        'event',
        'event_start_end',
        'event_location',
        'event_price',
        'submitted',
        'updated',
    ]
    fieldsets = (
        (
            'User',
            {
                'fields': (
                    'user',
                    'user_school',
                    'user_city',
                    'user_dietary_requirements',
                )
            },
        ),
        (
            'Event',
            {
                'fields': (
                    'event',
                    'event_start_end',
                    'event_location',
                )
            },
        ),
        (
            'Application',
            {
                'fields': (
                    'submitted',
                    'updated',
                    'status',
                    'applicant_type',
                    'staff_comments',
                )
            },
        ),
        (
            'Billing',
            {
                'fields': (
                    'event_price',
                    'paid',
                    'billing_physical_address',
                    'billing_email_address',
                )
            },
        ),
    )

    @admin.display(description="User's school")
    def user_school(self, application):
        return application.user.school

    @admin.display(description="User's city")
    def user_city(self, application):
        return application.user.city

    @admin.display(description="User's dietary requirements")
    def user_dietary_requirements(self, application):
        return format_html_join(
            '\n',
            '<li>{}</li>',
            application.user.dietary_requirements.values_list('name'),
        )

    @admin.display
    def event_start_end(self, application):
        return f'{application.event.start} to {application.event.end}'

    @admin.display
    def event_location(self, application):
        return application.event.location_summary()

    @admin.display
    def event_price(self, application):
        return f'${application.event.price:.2f}'



admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin),
admin.site.register(Series),
admin.site.register(Session),
admin.site.register(EventApplication, EventApplicationAdmin),
admin.site.register(RegistrationForm),
admin.site.register(ApplicantType),
