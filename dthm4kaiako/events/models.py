"""Models for events registration."""

from django.db import models
from django.contrib.gis.db import models as geomodels
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.timezone import now
from utils.get_upload_filepath import get_event_series_upload_path
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from users.models import Entity, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from utils.new_zealand_regions import REGION_CHOICES, REGION_CANTERBURY
import datetime
import re

DATETIME_HELP_TEXT = "Desired format is YYYY-MM-DD hh:mm:ss, e.g. 2022-06-09 11:30:00 (9th May 2022 at 11.30am)"


class Location(models.Model):
    """Model for a physical location."""

    room = models.CharField(
        max_length=200,
        blank=True,
        help_text='Name of room or space, for example: Room 134',
    )
    name = models.CharField(
        max_length=200,
        help_text='Name of location, for example: Middleton Grange School'
    )
    street_address = models.CharField(
        max_length=200,
        blank=True,
        help_text='Street address location, for example: 12 High Street'
    )
    suburb = models.CharField(
        max_length=200,
        blank=True,
        help_text='Suburb, for example: Riccarton'
    )
    city = models.CharField(
        max_length=200,
        help_text='Town or city, for example: Christchurch',
        default='Christchurch',
    )
    region = models.PositiveSmallIntegerField(
        choices=REGION_CHOICES,
        default=REGION_CANTERBURY,
    )
    description = RichTextUploadingField(blank=True)
    coords = geomodels.PointField()

    def __str__(self):
        """Text representation of a location."""
        return self.get_full_address()

    def get_absolute_url(self):
        """Return URL of location on website.

        Returns:
            URL as a string.
        """
        return reverse('events:location', kwargs={'pk': self.pk})

    def get_full_address(self):
        """Get full text representation of a location."""
        address = ''
        if self.room:
            address += self.room + ',\n'
        address += self.name + ',\n'
        if self.street_address:
            address += self.street_address + ',\n'
        if self.suburb:
            address += self.suburb + ', '
        address += self.city + ',\n'
        address += self.get_region_display()
        return address

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]


class Series(models.Model):
    """Model for an event series."""

    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=30)
    description = RichTextUploadingField()
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_series_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )

    def __str__(self):
        """Text representation of an event series."""
        return self.name

    def save(self, *args, **kwargs):
        """Override save method to ensure logo is saved to correct directory.

        The method saves the file once the instance has a primary key,
        as the upload_to function of the file uses this key.

        This method is adapted from the answer at:
        https://stackoverflow.com/a/58853713/10345299
        """
        if self.pk is None:
            saved_image = self.logo
            self.logo = None
            super().save(*args, **kwargs)
            self.logo = saved_image
            kwargs.pop('force_insert', None)
        super().save(*args, **kwargs)

    class Meta:
        """Meta options for class."""

        verbose_name_plural = "series"


class ParticipantType(models.Model):
    """Model for event participant type.

    For example: event staff, facilitator, teacher, student, with
    costs e.g. $0 for free or say $40 to attend.

    This is usually for events that require event registrations to be approved i.e. paid
    """

    name = models.CharField(max_length=200, help_text="Participant type e.g. teacher, event staff")
    price = models.FloatField(help_text="Cost for participant type to attend in NZD")

    class Meta:
        """Meta options for class."""

        unique_together = ('name', 'price',)
        ordering = ['name', ]
        verbose_name_plural = 'participant type'

    def __str__(self):
        """Text representation of a participant type with their participant price."""
        if self.is_free():
            return f"{self.name} (free)"
        else:
            return f"{self.name} (${'{0:.2f}'.format(float(self.price))})"

    def is_free(self):
        """Determine whether the event participant type is free or not.

        Returns True if participant type is free.
        """
        return '{0:.2f}'.format(float(self.price)) == "0.00"

    def clean(self):
        """Validate participant type model attributes.

        Raises:
            ValidationError if invalid attributes.
        """

        price_pattern_with_decimal_places = re.compile(r"[^\d+(\.\d{2})?]$") # TODO: requires refinement

        if price_pattern_with_decimal_places.match(f'{0:.2f}'.format(str(self.price))):
            raise ValidationError(
                {
                    'price':
                    _('Price must be be in the form of $1.23 or $1.')
                }
            )


class Event(models.Model):
    """Model for an event."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField(
        help_text="This is the description that will appear on this event's page that participants will view."
        )
    slug = AutoSlugField(populate_from='get_short_name', always_update=True, null=True)
    # TODO: Only allow publishing if start and end are not null
    published = models.BooleanField(default=False)
    show_schedule = models.BooleanField(
        default=False,
        help_text="Select if you would like to show this event's schedule to prospective event participants."
        )
    featured = models.BooleanField(default=False, help_text="Select if this event is a featured event.")
    REGISTRATION_TYPE_REGISTER = 1
    REGISTRATION_TYPE_APPLY = 2
    REGISTRATION_TYPE_EXTERNAL = 3
    REGISTRATION_TYPE_INVITE_ONLY = 4
    REGISTRATION_TYPE_CHOICES = (
        (REGISTRATION_TYPE_REGISTER, _('Register to attend event (Registrations auto-approved)')),
        (REGISTRATION_TYPE_APPLY, _('Register to attend event (Manual approval required)')),
        (REGISTRATION_TYPE_EXTERNAL, _('Visit external event website')),
        (REGISTRATION_TYPE_INVITE_ONLY, _('This event is invite only')),
    )
    registration_type = models.PositiveSmallIntegerField(
        choices=REGISTRATION_TYPE_CHOICES,
        default=REGISTRATION_TYPE_REGISTER,
        help_text="Register type events will not require you to " +
        "approve or reject event reigstration forms.\n\n" +
        "Apply type events require you to approve event " +
        "registrations in order for a participant to be attending this event."
    )
    external_event_registration_link = models.URLField(
        blank=True,
        null=True,
        help_text=(
            "Only required when the event registration type is 'external'. \n\n" +
            "This is a link to an external location that "
            "will gather event registrations' information e.g. Google Form"
        )
    )
    # TODO: Cannot be null if published or event registrations exist
    start = models.DateTimeField(
        blank=True,
        null=True,
        help_text=DATETIME_HELP_TEXT
    )
    # TODO: Cannot be null if published or event registrations exist
    end = models.DateTimeField(
        blank=True,
        null=True,
        help_text=DATETIME_HELP_TEXT
    )
    accessible_online = models.BooleanField(
        default=False,
        help_text='Select if this participants will be attending this online e.g. Zoom'
    )
    locations = models.ManyToManyField(
        Location,
        related_name='events',
        blank=True,
        help_text="To select multiple event locations, hold CONTROL and click to select the locations."
    )
    sponsors = models.ManyToManyField(
        Entity,
        related_name='sponsored_events',
        blank=True,
        help_text="To select multiple event sponsors, hold CONTROL and click to select the sponsors."
    )
    organisers = models.ManyToManyField(
        Entity,
        related_name='events',
        blank=True,
        help_text="To select multiple event organisers, hold CONTROL and click to select the sponsors."
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True,
        help_text="Optional. Select the series the event is a part of if it applies."
    )
    is_catered = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text="Select if food will be provided at this event. " +
        "Participants will be ask for their dietary requirements when registering/applying"
    )
    contact_email_address = models.EmailField(
        max_length=150,
        blank=False,
        null=False,
        default='',
        help_text="The email which event participants can contact you via."
    )
    event_staff = models.ManyToManyField(
        User,
        related_name='events',
        blank=True,
        help_text="To select multiple event staff members, hold CONTROL and click to select the individuals."
    )
    is_cancelled = models.BooleanField(
        default=False,
        null=False,
        help_text='This event has been cancelled'
    )
    participant_types = models.ManyToManyField(
        ParticipantType,
        related_name='events',
        blank=True,
        help_text="The participant types that will be available for event participants to choose from."
    )
    capacity = models.IntegerField(
        default=1,
        help_text="What is the maximum number of people who can attend this event?"
    )

    # TODO: Add validation that if no locations, then accessible_online must be True
    # See: https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.m2m_changed

    def update_datetimes(self):
        """Update datetimes of event."""
        self.start = self.sessions.order_by('start').first().start
        self.end = self.sessions.order_by('-end').first().end
        self.save()

    def get_absolute_url(self):
        """Return URL of event on website.

        Returns:
            URL as a string.
        """
        return reverse('events:event', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_short_name(self):
        """Event name with series abbreviation if available.

        Returns:
            String of short event name.
        """
        if self.series:
            return '{}: {}'.format(self.series.abbreviation, self.name)
        else:
            return self.name

    def location_summary(self):
        """Return string of event location.

        Returns:
            String of summary of event location or None if no locations.
        """
        locations = list(self.locations.all())
        if len(locations) > 1:
            return 'Multiple locations'
        elif locations:
            location = locations[0]
            return '{}, {}'.format(location.city, location.get_region_display())
        else:
            return None

    def save(self, *args, **kwargs):
        """Save the event."""
        return super().save(*args, **kwargs)

    @property
    def is_register_or_apply(self):
        """Return True if the event is an event which users can register or apply to attend.

        Returns:
            Boolean if the event is an event which users can register or apply to attend.
        """
        return self.registration_type in {self.REGISTRATION_TYPE_APPLY, self.REGISTRATION_TYPE_REGISTER}

    @property
    def get_registration_button_text(self):
        """Return True if the event is an event which users can register or apply to attend.

        Returns:
            Boolean if the event is an event which users can register or apply to attend.
        """
        if self.registration_type == self.REGISTRATION_TYPE_APPLY:
            return "Apply to attend event"
        elif self.registration_type == self.REGISTRATION_TYPE_REGISTER:
            return "Register to attend event"
        else:
            return ""

    @property
    def has_ended(self):
        """Return True if event has ended.

        Returns:
            Boolean if event has ended.
        """
        if self.end is not None:
            return now() > self.end

    @property
    def get_event_type_short(self):
        """Return 'Apply' if the registration type is apply or 'Register' if it is register.

        Returns:
            String
        """
        if self.registration_type == self.REGISTRATION_TYPE_APPLY:
            return "Apply"
        elif self.registration_type == self.REGISTRATION_TYPE_REGISTER:
            return "Register"
        elif self.registration_type == self.REGISTRATION_TYPE_INVITE_ONLY:
            return "Invite only"
        elif self.registration_type == self.REGISTRATION_TYPE_EXTERNAL:
            return "External"

    @property
    def get_event_type_short_updating(self):
        """Return string to update form.

        Returns:
            String.
            'Update registration form' if the registration type is apply.
            'Update registration form' if it is register.
        """
        if self.registration_type == self.REGISTRATION_TYPE_APPLY:
            return "Update registration form"
        elif self.registration_type == self.REGISTRATION_TYPE_REGISTER:
            return "Update registration form"
        else:
            return ""

    @property
    def start_weekday_name(self):
        """Return the weekday name of the start date of the event.

        For example, "Wednesday".
        """
        return self.start.strftime('%A')

    @property
    def is_less_than_one_week_prior_event(self):
        """Return true if there is less than a week until the event commencing.

        This is so that a catering order for the event can be finalised a week before the event starts.
        Flase is returned if the current date is exactly one week prior to the event start datetime.
        """
        today_tz = datetime.datetime.today()
        today = today_tz.replace(tzinfo=None)
        one_week_prior_event_start = self.start - datetime.timedelta(days=7)
        return today.isoformat() > one_week_prior_event_start.isoformat()

    @property
    def registration_status_counts(self):
        """Count the number of event registrations with each of the possible statuses.

        Includes:
            - "Pending" (1)
            - "Approved" (2)
            - "Declined" (3)
            - "Withdrawn" (4)

        Returns a dictionary of the counts.
        """
        status_counts = {
            'pending': 0,
            'approved': 0,
            'declined': 0,
            'withdrawn': 0
        }
        event_registrations = EventRegistration.objects.filter(event=self)

        for registration in event_registrations:

            if registration.status == 1:
                status_string = 'pending'
            elif registration.status == 2:
                status_string = 'approved'
            elif registration.status == 3:
                status_string = 'declined'

            status_counts[status_string] += 1

        status_counts['withdrawn'] = DeletedEventRegistration.objects.filter(event=self).count()

        return status_counts

    @property
    def participant_type_counts(self):
        """Count the number of event participants per type."""
        participant_type_counts = {}
        registrations = EventRegistration.objects.filter(event=self.pk)

        for participant_type in self.participant_types.all():
            key_string = str(participant_type)
            participant_type_counts[key_string] = 0

        for registration in registrations:
            key_string = str(registration.participant_type)
            if key_string in participant_type_counts:
                participant_type_counts[key_string] += 1

        return participant_type_counts

    @property
    def participant_type_counts_approved(self):
        """Count the number of event participants per type."""
        participant_type_counts = {}
        APPROVED = 2
        registrations = EventRegistration.objects.filter(event=self.pk, status=APPROVED)

        for participant_type in self.participant_types.all():
            key_string = str(participant_type)
            participant_type_counts[key_string] = 0

        for registration in registrations:
            key_string = str(registration.participant_type)
            if key_string in participant_type_counts:
                participant_type_counts[key_string] += 1

        return participant_type_counts

    @property
    def reasons_for_withdrawing_counts(self):
        """Count the number of each reason for an event registration to be withdrawn.

        Returns a dictionary of the counts.
        """
        reason_counts = {
            'prefer_not_to_say': 0,
            'illness': 0,
            'not_interested': 0,
            'change_of_plans': 0,
            'too_expensive': 0,
            'inconvenient_location': 0,
            'other': 0,
            'wrong_event': 0,
            'clash_of_personal_development': 0
        }
        deleted_event_registrations = DeletedEventRegistration.objects.filter(event=self)

        for deleted_registration in deleted_event_registrations:

            if deleted_registration.withdraw_reason == 1:
                reason_string = 'prefer_not_to_say'
            elif deleted_registration.withdraw_reason == 2:
                reason_string = 'illness'
            elif deleted_registration.withdraw_reason == 3:
                reason_string = 'not_interested'
            elif deleted_registration.withdraw_reason == 4:
                reason_string = 'change_of_plans'
            elif deleted_registration.withdraw_reason == 5:
                reason_string = 'too_expensive'
            elif deleted_registration.withdraw_reason == 6:
                reason_string = 'inconvenient_location'
            elif deleted_registration.withdraw_reason == 7:
                reason_string = 'other'
            elif deleted_registration.withdraw_reason == 8:
                reason_string = 'wrong_event'
            elif deleted_registration.withdraw_reason == 9:
                reason_string = 'clash_of_personal_development'
            reason_counts[reason_string] += 1

        return reason_counts

    @property
    def other_reasons_for_withdrawing(self):
        """Return a list of reasons for why event registrations were withdrawn for the given event."""
        deleted_event_registrations = DeletedEventRegistration.objects.filter(event=self)
        other_reasons = []
        for deleted_event_registration in deleted_event_registrations:
            if deleted_event_registration.other_reason_for_withdrawing != "":
                other_reasons.append(deleted_event_registration.other_reason_for_withdrawing)
        return other_reasons

    def __str__(self):
        """Text representation of an event."""
        return self.name

    def clean(self):
        """Validate event model attributes.

        Raises:
            ValidationError if invalid attributes.
        """
        if self.registration_type == self.REGISTRATION_TYPE_INVITE_ONLY and self.external_event_registration_link:
            raise ValidationError(
                {
                    'external_event_registration_link':
                    _('Registration link must be empty when event is set to invite only.')
                }
            )

        if self.published and self.start is None:
            raise ValidationError(
                {
                    'start':
                    _('Start datetime is required when the event is published.')
                }
            )

        if self.published and self.end is None:
            raise ValidationError(
                {
                    'end':
                    _('End datetime is required when the event is published.')
                }
            )

        if self.capacity <= 0:
            raise ValidationError(
                {
                    'capacity':
                    _('Capacity must be a positive number.')
                }
            )

    class Meta:
        """Meta options for class."""

        ordering = ['start', 'end']

    @property
    def is_free(self):
        """Determine whether the event is free or not.

        This is based on the prices of the event's participants.
        If these are all free participants then the event is considered to be free.
        """
        free = True
        for participant_type in self.participant_types.all():
            if participant_type.price != 0.0:
                return False
        return free


class Session(models.Model):
    """Model for an event session."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField(blank=True)
    url = models.URLField(blank=True)
    url_label = models.CharField(max_length=200, blank=True)
    start = models.DateTimeField(help_text=DATETIME_HELP_TEXT)
    end = models.DateTimeField(help_text=DATETIME_HELP_TEXT)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='sessions',
    )
    locations = models.ManyToManyField(
        Location,
        related_name='sessions',
        blank=True,
    )
    facilitators = models.ManyToManyField(
        User,
        related_name='sessions',
        blank=True,
        verbose_name="Facilitators of this session"
    )

    def __str__(self):
        """Text representation of an session."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['start', 'end', 'name']


class Address(models.Model):
    """Model for an address.

    This is modelled off an NZ tax invoice.
    It is intended to be used for obtaining the billing address in the event registration form.
    """

    street_number = models.CharField(
        max_length=10,
        help_text='Street address\' number, for example: 12'
    )

    street_name = models.CharField(
        max_length=200,
        help_text='Street address\' name, for example: High Street'
    )
    suburb = models.CharField(
        max_length=200,
        help_text='Suburb, for example: Riccarton'
    )
    city = models.CharField(
        max_length=200,
        help_text='Town or city, for example: Christchurch',
        default='Christchurch',
    )
    region = models.PositiveSmallIntegerField(
        choices=REGION_CHOICES,
        default=REGION_CANTERBURY,
    )
    post_code = models.IntegerField(
        help_text='Post code, for example: 8041',
        default='8041',
    )
    country = models.CharField(
        max_length=300,
        default='New Zealand'
        )

    def __str__(self):
        """Text representation of an address."""
        return self.get_full_address()

    def get_full_address(self):
        """Get full text representation of an address."""
        address = '{} {},\n{},\n{},\n{}'.format(
            self.street_number,
            self.street_name,
            self.suburb,
            self.city,
            self.post_code
        )
        return address

    def clean(self):
        """Validate address model attributes.

        Raises:
            ValidationError if invalid attributes.
        """
        post_code_pattern = re.compile("^([0-9]){4}$")

        if not post_code_pattern.match(str(self.post_code)):
            raise ValidationError(
                {
                    'post_code':
                    _('Post code must be four digits.')
                }
            )

        street_number_pattern = re.compile("^([A-Za-z0-9])+$")

        if not street_number_pattern.match(str(self.street_number)):
            raise ValidationError(
                {
                    'street_number':
                    _('Street number can only include upper and lower case letters and numbers')
                }
            )


# TODO: consider pulling out emergency contact details into separate model
# TODO: make emergency contact details only mandatory for events that are in
# person i.e. don't show them for online events and allow them to be empty
class EventRegistration(models.Model):
    """Model for an event registration."""

    PENDING = 1
    APPROVED = 2
    DECLINED = 3
    APPLICATION_STATUSES = (
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (DECLINED, _('Declined')),
    )

    submitted = models.DateTimeField(auto_now_add=True)  # user does not edit
    updated = models.DateTimeField(auto_now=True)  # user does not edit
    status = models.PositiveSmallIntegerField(
        choices=APPLICATION_STATUSES,
        default=PENDING,
    )
    participant_type = models.ForeignKey(
        ParticipantType,
        on_delete=models.CASCADE,
        related_name='event_registrations',
        null=True,
        blank=True
    )
    staff_comments = models.TextField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    representing = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        default='',
        help_text='Who will you be repesenting at this event? e.g. school, organisation, association, myself'
        )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_registrations',
    )
    emergency_contact_first_name = models.CharField(
        max_length=200,
        verbose_name='emergency contact\'s first name',
        blank=True,
        null=True,
        default='',
        )
    emergency_contact_last_name = models.CharField(
        max_length=200,
        verbose_name='emergency contact\'s last name',
        blank=True,
        null=True,
        default='',
        )
    emergency_contact_relationship = models.CharField(
        max_length=150,
        verbose_name='relationship with emergency contact',
        blank=True,
        null=True,
        default='',
        )
    emergency_contact_phone_number = models.CharField(
        max_length=40,
        verbose_name='emergency contact\'s phone number',
        blank=True,
        null=True,
        default='',
        )
    paid = models.BooleanField(
        default=False
    )
    bill_to = models.CharField(
        max_length=200,
        null=False,
        default='',
        help_text="Who will be paying for this participant to attend?"
    )
    billing_physical_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='event_registrations',
        blank=True,
        null=True,  # since not needed for events that are free
        verbose_name='billing address',
    )
    billing_email_address = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
    )
    admin_billing_comments = models.TextField(blank=True)

    class Meta:
        """Meta options for class."""

        ordering = ['event', 'status']
        verbose_name_plural = 'event registrations'
        unique_together = ('event', 'user')

    def __str__(self):
        """Return string representation of an event registration."""
        return f'{self.user}'

    def clean(self):
        """Validate event registration model attributes.

        Raises:
            ValidationError if invalid attributes.
        """
        try:
            event = self.event
        except EventRegistration._meta.model.event.RelatedObjectDoesNotExist:
            event = None

        if (
            event is not None
            and self.event.accessible_online is False
            and self.emergency_contact_first_name is None
        ):
            raise ValidationError(
                {
                    'emergency_contact_first_name':
                    _(
                        'Emergency contact first name is required for in person event.'
                    )
                }
            )

        if (
            event is not None
            and self.event.accessible_online is False
            and self.emergency_contact_last_name is None
        ):
            raise ValidationError(
                {
                    'emergency_contact_last_name':
                    _(
                        'Emergency contact last name is required for in person event.'
                    )
                }
            )

        if (
            event is not None
            and self.event.accessible_online is False
            and self.emergency_contact_relationship is None
        ):
            raise ValidationError(
                {
                    'emergency_contact_relationship':
                    _(
                        'Emergency contact relationship is required for in person event.'
                    )
                }
            )

        if (
            event is not None
            and self.event.accessible_online is False
            and self.emergency_contact_phone_number is None
        ):
            raise ValidationError(
                {
                    'emergency_contact_phone_number':
                    _(
                        'Emergency contact phone number is required for in person event.'
                    )
                }
            )

        phone_number_pattern = re.compile(r"^[-\(\)\+\s\./0-9]*$")
        if (
            event is not None
            and self.event.accessible_online is False
            and not phone_number_pattern.match(str(self.emergency_contact_phone_number))
        ):
            raise ValidationError(
                {
                    'emergency_contact_phone_number':
                    _(
                        'Invalid phone number. Phone number can include the area code, follow by any '
                        'number of numbers, - and spaces. E.g. (+64) 123 45 678, 123-45-678, 12345678'
                    )
                }
            )

    @property
    def status_string_for_user(self):
        """Return event registration's status as a string.

        Returns:
            String to readability.
        """
        string_form = ""
        if self.status == 1:
            string_form = "Pending"
        elif self.status == 2:
            string_form = "Approved"
        elif self.status == 3:
            string_form = "Declined"
        return string_form


class DeletedEventRegistration(models.Model):
    """Model for a deleted event registration.

    It contains the bare minimum information so that there is no identifiable information.
    """

    PREFER_NOT_TO_SAY = 1
    ILLNESS = 2
    NOT_INTERESTED = 3
    CHANGE_OF_PLANS = 4
    TOO_EXPENSIVE = 5
    INCONVENIENT_LOCATION = 6
    OTHER = 7
    WRONG_EVENT = 8
    CLASH_OF_PERSONAL_DEVELOPMENT = 9
    WITHDRAW_REASONS = (
        (NOT_INTERESTED, _('No longer interested')),
        (CHANGE_OF_PLANS, _('Change of plans')),
        (TOO_EXPENSIVE, _('No funding')),
        (INCONVENIENT_LOCATION, _('Inconvient location')),
        (WRONG_EVENT, _('Wrong event')),
        (CLASH_OF_PERSONAL_DEVELOPMENT, _('Clash of personal development')),
        (ILLNESS, _('Illness')),
        (PREFER_NOT_TO_SAY, _('Prefer not to say')),
        (OTHER, _('Other'))
    )
    date_deleted = models.DateTimeField(
        auto_now_add=True,
        help_text="Date the original event registration was deleted"
    )
    withdraw_reason = models.PositiveSmallIntegerField(
        choices=WITHDRAW_REASONS,
        default=PREFER_NOT_TO_SAY,
        help_text="Reason the participant has chosen to withdraw their registration."
    )
    other_reason_for_withdrawing = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='deleted_event_registrations',
        default=""
    )

    def save(self, *args, **kwargs):
        """Override for save method.

        Override save to check that if the deletion reasons is 'other'
        that there is a related reason for this (not an empty string),
        otherwise, we change the reason from 'other' to 'prefer not to say'.
        """
        if self.withdraw_reason == 7 and not self.other_reason_for_withdrawing:
            self.withdraw_reason = 1
        super(DeletedEventRegistration, self).save(*args, **kwargs)


TERMS_AND_CONDITIONS_DEFAULT = (
    "<p>Expenses for travel and accommodation are not covered by the event organisers, and "
    "are to be organised by the attendees themselves. Event organisers may provide details "
    "of available funding options that attendees&rsquo; may apply for.</p> <p>Should you need "
    "to cancel your registration/registration, please let us know as soon as possible and "
    "we&#39;ll remove it. If you do not show to the event without informing us, you may be "
    "liable for a &lsquo;did not show&rsquo; fee. We understand life happens.</p> <p>In the "
    "event of cancellation of the event, we will notify you as soon as possible. It is your "
    "responsibility to understand any cancellation clauses for your flights and accommodation. "
    "While we are sorry if this causes inconvenience, the organisers will not be liable for "
    "any loss, damages, or sadness arising from such changes.</p> <p>Please be aware the event "
    "organisers and attendees may be taking photographs, video, and/or audio to record events. "
    "These may be displayed on websites or social media for education and/or promotional "
    "purposes. By attending the event you understand that these images and recordings may be "
    "used by the event organisers for related marketing and promotions. You understand that if "
    "you do not wish to have your image or voice recorded you must inform any media person "
    "taking your photo, videoing you, or recording your voice at the workshop. It is your "
    "responsibility to remove yourself from the photo, video, or voice recording situations. "
    "Photographers will do their best to take group images that do not identify people and will "
    "seek permission in particular instances where close ups are taken. Attendees posting on "
    "social media will be asked to check with you first, before posting. The event organisers "
    "does not accept responsibility for media posted by attendees.</p> <p>By registering for this "
    "event, you agree to us storing your information for organising and running the event. You "
    "are required to follow all health and safety instructions from event organisers while "
    "attending the event.</p> <p>Finally, you agree to and understand with the terms and "
    "conditions regarding the Code of Conduct. Read our Code of Conduct here: "
    "https://gist.github.com/uccser-admin/56de956a32ccf68e253be8632957c014</p>"
)


class RegistrationForm(models.Model):
    """Model for a registration form."""

    open_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="This is the date and time that participants " +
        "can begin registering for this event.\n\n" + DATETIME_HELP_TEXT)
    close_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="This is the date and time that participants " +
        "registerations close for this event.\n\n" + DATETIME_HELP_TEXT)
    terms_and_conditions = RichTextUploadingField(
        default=TERMS_AND_CONDITIONS_DEFAULT,
        help_text="Event participants must agree to this to register/apply for this event.")
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="registration_form"
    )

    def get_absolute_url(self):
        """Return URL of event registration form on website.

        Returns:
            URL as a string.
        """
        return reverse('events:register', kwargs={'pk': self.event.pk})

    def __str__(self):
        """Text representation of an event registration form."""
        return f'{self.event.name}'

    # TODO: test these
    def clean(self):
        """Validate event registration form model attributes.

        Raises:
            ValidationError if invalid attributes.
        """
        if self.open_datetime is not None and self.open_datetime < now() and self.event.published is False:
            # Prior publishing, organiser must ensure the open date is in the future.
            # After publishing, open date can be in the past as the organiser will possibly update the close date time.
            raise ValidationError(
                {
                    'open_datetime':
                    _('Open datetime must be in the future')
                }
            )

        if self.close_datetime is not None and self.close_datetime <= self.open_datetime:
            raise ValidationError(
                {
                    'close_datetime':
                    _('Close datetime must be after the open datatime')
                }
            )

        if self.open_datetime is not None and self.event.participant_types.count() == 0:
            raise ValidationError(
                {
                    'open_datetime':
                    _('At least one participant type is required for registrations to open.')
                }
            )

        if self.close_datetime and self.close_datetime >= self.event.start:
            raise ValidationError(
                {
                    'close_datetime':
                    _('Close datetime must be before the event\'s start time')
                }
            )

    def save(self, *args, **kwargs):
        """Do a full clean prior to saving the registration form."""
        self.full_clean()
        return super(RegistrationForm, self).save(*args, **kwargs)


@receiver(post_save, sender=Event)
def create_registration_form(sender, instance, created, **kwargs):
    """Create a registration form when an event is created."""
    if created:
        RegistrationForm.objects.create(event=instance)
