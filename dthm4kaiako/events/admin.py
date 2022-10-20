"""Module for admin configuration for the events application."""
import logging
from django.contrib import admin
from django.utils.timezone import now
from django.contrib.gis.db import models as geomodels
from django.utils.translation import gettext_lazy as _
from events.models import (
    DeletedEventRegistration,
    Event,
    Session,
    Location,
    Series,
    EventRegistration,
    RegistrationForm,
    ParticipantType,
)
from mapwidgets.widgets import GooglePointFieldWidget
from modelclone import ClonableModelAdmin
from django.utils.html import format_html_join
import datetime

datetime_str = '2016-05-18T15:37:36.993048Z'
old_format = '%Y-%m-%dT%H:%M:%S.%fZ'
new_format = '%d-%m-%Y %H:%M:%S'

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
                    'start',
                    'end',
                    'series',
                    'organisers',
                    'sponsors',
                    'participant_types',
                    'is_catered',
                    'contact_email_address',
                    'capacity',
                )
            }
        ),
        ('Location', {
            'fields': ('accessible_online', 'locations'),
        }),
        ('Registration', {
            'description': 'Currently only registration via URL is available.',
            'fields': (
                'external_event_registration_link',
                'registration_type',
            ),
        }),
        ('Visibility', {
            'fields': (
                'published',
                'featured',
                'show_schedule',
                'is_cancelled'
            ),
        }),
        ('Permissions', {
            'fields': ('event_staff',),
        }),
    )
    filter_horizontal = (
        'organisers',
        'sponsors',
        'participant_types'
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


class EventRegistrationAdmin(admin.ModelAdmin):
    """Admin view for an event registration."""

    model = EventRegistration
    readonly_fields = [
        'user',
        'user_education_entities',
        'user_region',
        'mobile_phone_number',
        'medical_notes',
        'user_dietary_requirements',
        'event',
        'event_start_end',
        'event_location',
        'submitted',
        'updated',
        'billing_physical_address',
        'billing_email_address',
        'email_address',
        'emergency_contact_first_name',
        'emergency_contact_last_name',
        'emergency_contact_relationship',
        'emergency_contact_phone_number',
        'bill_to',
    ]
    fieldsets = (
        (
            'User',
            {
                'fields': (
                    'user',
                    'user_education_entities',
                    'user_region',
                    'mobile_phone_number',
                    'email_address',
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
            'Registration',
            {
                'fields': (
                    'submitted',
                    'updated',
                    'status',
                    'participant_type',
                    'representing',
                    'medical_notes',
                    'staff_comments',
                    'emergency_contact_first_name',
                    'emergency_contact_last_name',
                    'emergency_contact_relationship',
                    'emergency_contact_phone_number',
                )
            },
        ),
        (
            'Billing',
            {
                'fields': (
                    'paid',
                    'bill_to',
                    'billing_physical_address',
                    'billing_email_address',
                )
            },
        ),
    )

    @admin.display(description="Educational entities participant belongs to")
    def user_education_entities(self, registration):
        """Return the education entities that the user is associated with."""
        return format_html_join(
            '\n',
            '<li>{}</li>',
            registration.user.educational_entities.values_list('name'),
        )

    @admin.display(description="User's region")
    def user_region(self, registration):
        """Return the user's region."""
        return registration.user.region

    @admin.display(description="User's dietary requirements")
    def user_dietary_requirements(self, registration):
        """Return the user's dietary requirements as a bullet point list."""
        return format_html_join(
            '\n',
            '<li>{}</li>',
            registration.user.dietary_requirements.values_list('name'),
        )

    @admin.display
    def event_start_end(self, registration):
        """Return the event's start and end dates."""
        date_time_start_str = registration.event.start.strftime("%d %b %Y, %I:%M %p")
        date_time_end_str = registration.event.end.strftime("%d %b %Y, %I:%M %p")
        return f'{date_time_start_str} to {date_time_end_str}'

    @admin.display
    def event_location(self, registration):
        """Return the event's location."""
        return registration.event.location_summary()

    @admin.display
    def mobile_phone_number(self, registration):
        """Return the event participant's mobile number."""
        return registration.user.mobile_phone_number

    @admin.display
    def medical_notes(self, registration):
        """Return the event participant's medical notes."""
        return registration.user.medical_notes

    @admin.display
    def participant_email_address(self, registration):
        """Return participant's email address."""
        return registration.event_registration.participant_email_address

    @admin.display
    def emergency_contact_first_name(self, registration):
        """Return the event participant's emergency contact's first name."""
        return registration.event_registration.emergency_contact_first_name

    @admin.display
    def emergency_contact_last_name(self, registration):
        """Return the event participant's emergency contact's last name."""
        return registration.event_registration.emergency_contact_last_name

    @admin.display
    def emergency_contact_relationship(self, registration):
        """Return the emergency contact's relationship with the event participant."""
        return registration.event_registration.emergency_contact_relationship

    @admin.display
    def emergency_contact_phone_number(self, registration):
        """Return the emergency contact's phone number of the event participant."""
        return registration.event_registration.emergency_contact_phone_number

    @admin.display
    def bill_to(self, registration):
        """Return the name of the entity who will pay for the event participant to attend."""
        return registration.event_registration.bill_to

    @admin.display
    def email_address(self, registration):
        """Return user's email address."""
        return registration.user.email_address


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin),
admin.site.register(Series),
admin.site.register(Session),
admin.site.register(EventRegistration, EventRegistrationAdmin),
admin.site.register(RegistrationForm),
admin.site.register(DeletedEventRegistration)
admin.site.register(ParticipantType)
