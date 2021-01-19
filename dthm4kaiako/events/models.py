"""Models for resources application."""


from django.db import models
from django.contrib.gis.db import models as geomodels
from django.core.exceptions import ValidationError
from django.urls import reverse
from utils.get_upload_filepath import get_event_series_upload_path
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from users.models import Entity


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
    REGION_NORTHLAND = 1
    REGION_AUCKLAND = 2
    REGION_WAIKATO = 3
    REGION_BAY_OF_PLENTY = 4
    REGION_GISBORNE = 5
    REGION_HAWKES_BAY = 6
    REGION_TARANAKI = 7
    REGION_MANAWATU_WANGANUI = 8
    REGION_WELLINGTON = 9
    REGION_TASMAN = 10
    REGION_NELSON = 11
    REGION_MARLBOROUGH = 12
    REGION_WEST_COAST = 13
    REGION_CANTERBURY = 14
    REGION_OTAGO = 15
    REGION_SOUTHLAND = 16
    REGION_CHATHAM_ISLANDS = 17
    REGION_CHOICES = (
        (REGION_NORTHLAND, _('Northland region')),
        (REGION_AUCKLAND, _('Auckland region')),
        (REGION_WAIKATO, _('Waikato region')),
        (REGION_BAY_OF_PLENTY, _('Bay of Plenty region')),
        (REGION_GISBORNE, _('Gisborne region')),
        (REGION_HAWKES_BAY, _("Hawke's Bay region")),
        (REGION_TARANAKI, _('Taranaki region')),
        (REGION_MANAWATU_WANGANUI, _('Manawatu-Wanganui region')),
        (REGION_WELLINGTON, _('Wellington region')),
        (REGION_TASMAN, _('Tasman region')),
        (REGION_NELSON, _('Nelson region')),
        (REGION_MARLBOROUGH, _('Marlborough region')),
        (REGION_WEST_COAST, _('West Coast region')),
        (REGION_CANTERBURY, _('Canterbury region')),
        (REGION_OTAGO, _('Otago region')),
        (REGION_SOUTHLAND, _('Southland region')),
        (REGION_CHATHAM_ISLANDS, _('Chatman Islands')),
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

    class Meta:
        """Meta options for class."""

        verbose_name_plural = "series"


class Event(models.Model):
    """Model for an event."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    slug = AutoSlugField(populate_from='get_short_name', always_update=True, null=True)
    # TODO: Only allow publishing if start and end are not null
    published = models.BooleanField(default=False)
    show_schedule = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    REGISTRATION_TYPE_REGISTER = 1
    REGISTRATION_TYPE_APPLY = 2
    REGISTRATION_TYPE_EXTERNAL = 3
    REGISTRATION_TYPE_INVITE_ONLY = 4
    REGISTRATION_TYPE_CHOICES = (
        (REGISTRATION_TYPE_REGISTER, _('Register to attend event')),
        (REGISTRATION_TYPE_APPLY, _('Apply to attend event')),
        (REGISTRATION_TYPE_EXTERNAL, _('Visit event website')),
        (REGISTRATION_TYPE_INVITE_ONLY, _('This event is invite only')),
    )
    registration_type = models.PositiveSmallIntegerField(
        choices=REGISTRATION_TYPE_CHOICES,
        default=REGISTRATION_TYPE_REGISTER,
    )
    registration_link = models.URLField(blank=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    accessible_online = models.BooleanField(
        default=False,
        help_text='Select if this event be attended online'
    )
    price = models.PositiveSmallIntegerField(default=0)
    locations = models.ManyToManyField(
        Location,
        related_name='events',
        blank=True,
    )
    sponsors = models.ManyToManyField(
        Entity,
        related_name='sponsored_events',
        blank=True,
    )
    organisers = models.ManyToManyField(
        Entity,
        related_name='events',
        blank=True,
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True,
    )
    applications = models.ForeignKey(
        EventApplication,
        on_delete=models.CASCADE,
        related_name='event',
        blank=True,
    )
    applicant_types = models.ManyToManyField(
        ApplicantType,
        related_name='events',
        blank=True,
    )
    # TODO: Add validation that if no locations, then accessible_online must be true
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

    def __str__(self):
        """Text representation of an event."""
        return self.name

    def clean(self):
        """Validate event model attributes.

        Raises:
            ValidationError if invalid attributes.
        """
        if self.registration_type == self.REGISTRATION_TYPE_INVITE_ONLY and self.registration_link:
            raise ValidationError(
                {
                    'registration_link':
                    _('Registration link must be empty when event is set to invite only.')
                }
            )
        if not self.registration_type == self.REGISTRATION_TYPE_INVITE_ONLY and not self.registration_link:
            raise ValidationError(
                {
                    'registration_link':
                    _('Registration link must be given when event is not set to invite only.')
                }
            )

    class Meta:
        """Meta options for class."""

        ordering = ['start', 'end']


class Session(models.Model):
    """Model for an event session."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField(blank=True)
    url = models.URLField(blank=True)
    url_label = models.CharField(max_length=200, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
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

    def __str__(self):
        """Text representation of an session."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['start', 'end', 'name']


class EventApplication(models.Model):
    """Model for an event application."""

    datetime_submitted = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    STATUS_PENDING = 'P'
    STATUS_ACCEPTED = 'A'
    STATUS_CANCELLED = 'C'
    STATUS_DECLINED = 'D'
    STATUS_CHOICES = (
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACCEPTED, _('Accepted')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_DECLINED, _('Declined')),
    )
    status = models.CharField(
        max_length=1,
        choices = STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    voucher = models.OneToOneField(
        Voucher,
        on_delete=models.CASCADE
    )
    # TODO: Might not need this field if we have Event object as foreign key
    vouchers = models.CharField(max_length=100, blank=True)
    staff_comments = models.CharField(max_length=500, blank=True)


class ApplicantType(models.Model):
    """Model for the applicant type. E.g. staff, attendee, vendor."""

    name = models.CharField(max_length=200)
    cost = models.FloatField()
    applications = models.ForeignKey(
        EventApplication,
        on_delete=models.CASCADE,
        related_name='applicant_type'
    )


class RegistrationForm(models.Model):
    """Model for a registration form."""

    datetime_open = models.DateTimeField()
    datetime_end = models.DateTimeField()
    session_choices = models.ForeignKey(
        RegistrationFormSessionChoice,
        on_delete=models.CASCADE,
        related_name='registraion_form',
    )
    terms_and_conditions = models.TextField()
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE
    )


class RegistrationFormSessionChoice(models.Model):
    """Model for sessions that run at the same time."""

    description = models.CharField(max_length=300, blank=True)
    sessions = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='form_choices',
    )


class EventVoucher(models.Model):
    """Model for an event voucher."""

    code = models.CharField(
        max_length=20,
        primary_key=True
    )
    active = models.BooleanField(default=False)
    new_cost = models.FloatField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='vouchers'
    )
