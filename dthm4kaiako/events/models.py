"""Models for events application."""


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
import datetime
from django.core.validators import MinLengthValidator, MaxLengthValidator


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
    registration_link = models.URLField(blank=True, null=True)
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
        return super().save(*args, **kwargs)

    #TODO: use this function instead of including logic in template to improve tidiness
    @property
    def is_register_or_apply(self):
        """ Returns True if the event is an event which users can register or apply to attend.

            Returns:
                Boolean if the event is an event which users can register or apply to attend.
        """
        return self.registration_type == self.REGISTRATION_TYPE_APPLY or self.registration_type == self.REGISTRATION_TYPE_REGISTER

    @property
    def has_ended(self):
        """Return True if event has ended.

        Returns:
            Boolean if event has ended.
        """
        return now() > self.end

    @property
    def get_event_type_short(self):
        """ Returns 'Apply' if the registration type is apply or 'Register' if it is register.

        Returns:
            String
        """

        if self.registration_type == self.REGISTRATION_TYPE_APPLY:
            return "Apply"
        elif self.registration_type == self.REGISTRATION_TYPE_REGISTER:
            return "Register"

    @property
    def has_attendance_fee(self):
        """ Determine if the event costs to attend.

        Returns:
            Boolean, True if the attendance has a cost.
        """
        return self.price != 0

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


class ApplicantType(models.Model):
    """Model for an application type.
       Alternative name would be 'TicketType', e.g. front section ticket, back section ticket, or student ticket, staff ticket."""
    name = models.CharField(max_length=100)
    cost = models.PositiveSmallIntegerField(default=0)
    event = models.ForeignKey(
        Event,
        related_name="application_types",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        """Text representation of an application type."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]
        verbose_name_plural = 'application type'


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
    post_code = models.IntegerField(
        validators=[MaxLengthValidator(4),MinLengthValidator(4)],
        help_text='Post code, for example: 8041',
        default='8041',)
    country = models.CharField(
        max_length=300,
        default='New Zealand'
        )
    

    def __str__(self):
        """Text representation of an address."""
        return self.get_full_address()


    def get_full_address(self):
        """Get full text representation of an address."""
        address = self.street_number + ' ' + self.street_name + ',\n' + self.suburb + ', ' + self.city + ',\n' + self.post_code + ',\n' + self.country
        return address


class EventApplication(models.Model):
    """Model for an event application."""

    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    WITHDRAWN = 4
    APPLICATION_STATUSES = (
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (WITHDRAWN, _('Withdrawn')),
    )

    submitted = models.DateTimeField(auto_now_add=True) # user does not edit
    updated = models.DateTimeField(auto_now=True) # user does not edit
    status = models.PositiveSmallIntegerField(
        choices=APPLICATION_STATUSES,
        default=PENDING,
    )
    applicant_type = models.ForeignKey(
        ApplicantType,
        on_delete=models.CASCADE,
        related_name='event_applications',
        null=True,
        blank=True
    )
    staff_comments = models.TextField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_applications'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_applications',
    )
    paid = models.BooleanField(default=False) #TODO: use a computed function for this
    billing_physical_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='event_applications',
        blank=True,
        null=True,
        verbose_name='billing address',
    )
    billing_email_address = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
        default='',
    )

    class Meta:
        """Meta options for class."""

        ordering = ['event', 'status']
        verbose_name_plural = 'event applications'
        unique_together = ('event', 'user')


    def __str__(self):
        """String representation of an event application."""
        return f'{self.event.name} - {self.user} - {self.status_string_for_user}'

    @property
    def status_string_for_user(self):
        """Return event application's status as a string.

        Returns:
            String to readability.
        """
        string_form = ""
        if self.status == 1:
            string_form = "Pending"
        elif self.status == 2:
            string_form = "Approved"
        elif self.status == 3:
            string_form = "Rejected"
        return string_form

    def withdraw(self):
        """Set the status to withdrawn."""
        self.status = 4


class RegistrationForm(models.Model):
    """Model for a registration form."""
    open_datetime = models.DateTimeField(null=True,blank=True) # TODO: sanity test these
    close_datetime = models.DateTimeField(null=True,blank=True) # TODO: sanity test these
    terms_and_conditions = models.TextField(blank=True)
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
        return reverse('events:event_registration', kwargs={'pk': self.event.pk, 'slug': self.event.slug})

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        """Text representation of an event registration form."""
        return f'{self.event.name}'

    
    # TODO: investigate why this is not working
    # def clean(self):
    #     """Validate event registration form model attributes.

    #     Raises:
    #         ValidationError if invalid attributes.
    #     """
    #     if now() > self.open_datetime:
    #         raise ValidationError(
    #             {
    #                 'open_datetime':
    #                 _('Open datetime must be in the future')
    #             }
    #         )

    #     if self.close_datetime < self.open_datetime:
    #         raise ValidationError(
    #             {
    #                 'close_datetime':
    #                 _('Close datetime must be after the open datatime')
    #             }
    #         )


@receiver(post_save, sender=Event)
def create_registration_form(sender, instance, created, **kwargs):
    """Create a registration form when an event is created."""
    if created:
        RegistrationForm.objects.create(event=instance)



