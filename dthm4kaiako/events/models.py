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
from utils.new_zealand_regions import REGION_CHOICES, REGION_CANTERBURY
import datetime
import re

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
    registration_link = models.URLField(blank=True, null=True, help_text="Optional. This is a link to an external location that will gather event applications' information e.g. Google Form")
    start = models.DateTimeField(blank=True, null=True, help_text="Desired format is YYYY-MM-DD hh:mm:ss, e.g. 2022-06-09 11:30:00 (9th May 2022 at 11.30am)")     # TODO: Cannot be null if published or event applications exist
    end = models.DateTimeField(blank=True, null=True, help_text="Desired format is YYYY-MM-DD hh:mm:ss, e.g. 2022-06-09 11:30:00 (9th May 2022 at 11.30am)")       # TODO: Cannot be null if published or event applications exist
    accessible_online = models.BooleanField( 
        default=False,
        help_text='Select if this event will be attended online'
    )
    is_free = models.BooleanField(
        default=False,
        help_text='Select if this event is free for all types of participants'
    )
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
    is_catered = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text='Select if food will be provided at this event'
    )
    contact_email_address = models.EmailField(
        max_length=150,
        blank=False,
        null=False,
        default='',
    )
    event_staff = models.ManyToManyField(
        User,
        related_name='events',
        blank=True,
    )
    is_cancelled = models.BooleanField(
        default=False,
        null=False,    
        help_text='This event has been cancelled'    
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
    def start_weekday_name(self):
        """
        Returns the weekday name of the start date of the event. 
        For example, "Wednesday".
        """
        return self.start.strftime('%A')

    @property
    def is_less_than_one_week_prior_event(self):
        """
        If there is less than a week until the event commences, returns True.
        This is so that a catering order for the event can be finalised a week before the event starts.
        Flase is returned if the current date is exactly one week prior to the event start datetime.
        """
        today_tz = datetime.datetime.today()
        today = today_tz.replace(tzinfo=None)
        one_week_prior_event_start = self.start - datetime.timedelta(days=7)
        one_week_prior_event_start = one_week_prior_event_start.replace(tzinfo=None)
        return today.isoformat() > one_week_prior_event_start.isoformat()


    @property
    def application_status_counts(self):
        """
        Counts the number of event applications with each of the possible statuses of "Pending" (1),
        "Approved" (2), "Rejected" (3) and "Withdrawn" (4).
        Returns a dictionary of the counts.
        """

        status_counts = {
            'pending' : 0,
            'approved' : 0,
            'rejected' : 0,
            'withdrawn' : 0
        }
        event_applications = EventApplication.objects.filter(event=self)

        for application in event_applications:

            if application.status == 1:
                status_string = 'pending'
            elif application.status == 2:
                status_string = 'approved'
            elif application.status == 3:
                status_string = 'rejected'

            status_counts[status_string] += 1

        status_counts['withdrawn'] = DeletedEventApplication.objects.filter(event=self).count()       

        return status_counts

    @property
    def reasons_for_withdrawing_counts(self):
        """
        Counts the number of each reason for an event application to be withdrawn.
        Returns a dictionary of the counts.
        """

        reason_counts = {
            'prefer_not_to_say' : 0,
            'illness' : 0,
            'not_interested' : 0,
            'change_of_plans' : 0,
            'too_expensive': 0,
            'inconvenient_location': 0,
            'other': 0
        }
        deleted_event_applications = DeletedEventApplication.objects.filter(event=self)

        for deleted_application in deleted_event_applications:

            if deleted_application.deletion_reason == 1:
                reason_string = 'prefer_not_to_say'
            elif deleted_application.deletion_reason == 2:
                reason_string = 'illness'
            elif deleted_application.deletion_reason == 3:
                reason_string = 'not_interested'
            elif deleted_application.deletion_reason == 4:
                reason_string = 'change_of_plans'
            elif deleted_application.deletion_reason == 5:
                reason_string = 'too_expensive'
            elif deleted_application.deletion_reason == 6:
                reason_string = 'inconvenient_location'
            elif deleted_application.deletion_reason == 7:
                reason_string = 'other'

            reason_counts[reason_string] += 1

        return reason_counts

    @property
    def other_reasons_for_withdrawing(self):
        """
        Returns a list of the other reasons for why event applications were withdrawn for the given event.
        """
        deleted_event_applications = DeletedEventApplication.objects.filter(event=self, deletion_reason=7)
        other_reasons = []
        for deleted_event_application in deleted_event_applications:
            other_reasons.append(deleted_event_application.other_reason_for_deletion)
        return other_reasons

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

        if self.published == True and self.start == None:
            raise ValidationError(
                {
                    'start':
                    _('Start datetime is required when the event is published.')
                }
            )
        
        if self.published == True and self.end == None:
            raise ValidationError(
                {
                    'end':
                    _('End datetime is required when the event is published.')
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
    facilitators = models.ManyToManyField(User, related_name='sessions', blank=True, verbose_name="Facilitators of this session")


    def __str__(self):
        """Text representation of an session."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['start', 'end', 'name']


class ParticipantType(models.Model):
    """Model for a participant type.
       Alternative name would be 'TicketType', e.g. front section ticket, back section ticket, or student ticket, staff ticket."""
    name = models.CharField(max_length=100)
    cost = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    event = models.ForeignKey(
        Event,
        related_name="participant_types",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        """Text representation of an participant type."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]
        verbose_name_plural = 'participant type'


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
        address = '{} {},\n{},\n{},\n{}'.format(self.street_number, self.street_name, self.suburb, self.city, self.post_code)
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


class EventApplication(models.Model):
    """Model for an event application."""

    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    APPLICATION_STATUSES = (
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )

    submitted = models.DateTimeField(auto_now_add=True) # user does not edit
    updated = models.DateTimeField(auto_now=True) # user does not edit
    status = models.PositiveSmallIntegerField(
        choices=APPLICATION_STATUSES,
        default=PENDING,
    )
    participant_type = models.ForeignKey(
        ParticipantType,
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
    representing = models.TextField(
        max_length=300,
        blank=False,
        null=False,
        default='',
        help_text='e.g. school, organisation, association, myself'
        )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_applications',
    )
    emergency_contact_first_name = models.CharField(
        max_length=50, 
        verbose_name='emergency contact\'s first name',
        blank=False,
        null=False,
        default='',
        )
    emergency_contact_last_name = models.CharField(
        max_length=50, 
        verbose_name='emergency contact\'s last name',
        blank=False,
        null=False,
        default='',
        )
    emergency_contact_relationship = models.CharField(
        max_length=150, 
        verbose_name='relationship with emergency contact',
        blank=False,
        null=False,
        default='',
        )
    emergency_contact_phone_number =  models.CharField(
        max_length=30, 
        verbose_name='emergency contact\'s phone number',
        blank=False,
        null=False,
        default='',
        )
    paid = models.BooleanField(
        default=False
    ) #TODO: use a computed function for this, based on participant types which have associated attendance fees
    bill_to = models.CharField(
        max_length=200, 
        blank=False,
        null=False,
        default='',
        help_text="Who will be paying for this participant to attend?"
    )
    billing_physical_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='event_applications',
        blank=True,
        null=True, # since not needed for events that are free
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
        verbose_name_plural = 'event applications'
        unique_together = ('event', 'user')


    def __str__(self):
        """String representation of an event application."""
        return f'{self.event.name} - {self.user} - {self.status_string_for_user}'


    def clean(self):
        """Validate event application model attributes.

        Raises:
            ValidationError if invalid attributes.
        """

        phone_number_pattern = re.compile("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")

        if not phone_number_pattern.match(str(self.emergency_contact_phone_number)):
            raise ValidationError(
                {
                    'emergency_contact_phone_number':
                    _('Phone number can include the area code, follow by any number of numbers, - and spaces. E.g. +(64) 123 45 678, 123-45-678, 12345678')
                }
            )


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


class DeletedEventApplication(models.Model):
    """
    Model for a deleted event application. 
    It contains the bare minimum information so that there is no identifiable information.
    """

    PREFER_NOT_TO_SAY = 1
    ILLNESS = 2
    NOT_INTERESTED = 3
    CHANGE_OF_PLANS = 4
    TOO_EXPENSIVE = 5
    INCONVENIENT_LOCATION = 6
    OTHER = 7
    WITHDRAW_REASONS = (
        (PREFER_NOT_TO_SAY, _('Prefer not to say')),
        (ILLNESS, _('Illness')),
        (NOT_INTERESTED, _('Not interested')),
        (CHANGE_OF_PLANS, _('Change of plans')),
        (TOO_EXPENSIVE, _('Too expensive / No funding')),
        (INCONVENIENT_LOCATION, _('Inconvient location')),
        (OTHER, _('Other')),
    )
    date_deleted = models.DateTimeField(
        auto_now_add=True,
        help_text="Date the original event application was deleted"
    )
    deletion_reason = models.PositiveSmallIntegerField(
        choices=WITHDRAW_REASONS,
        default=PREFER_NOT_TO_SAY,
        help_text="Reason the participant has chosen to withdraw their application."
    )
    other_reason_for_deletion = models.CharField(
        max_length = 300,
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='deleted_event_applications',
        default=""
    )

    def save(self, *args, **kwargs):
        """
        Override save to check that if the deletion reasons is 'other' 
        that there is a related reason for this (not an empty string), 
        otherwise, we change the reason from 'other' to 'prefer not to say'.
        """
        
        if self.deletion_reason == 7 and not self.other_reason_for_deletion:
            self.deletion_reason = 1
        super(DeletedEventApplication, self).save(*args, **kwargs)


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
        return reverse('events:apply', kwargs={'pk': self.event.pk,})

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        """Text representation of an event registration form."""
        return f'{self.event.name}'
    
    def clean(self):
        """Validate event registration form model attributes.

        Raises:
            ValidationError if invalid attributes.
        """
        if self.open_datetime != None and now() > self.open_datetime:
            raise ValidationError(
                {
                    'open_datetime':
                    _('Open datetime must be in the future')
                }
            )

        if self.close_datetime != None and self.close_datetime <= self.open_datetime:
            raise ValidationError(
                {
                    'close_datetime':
                    _('Close datetime must be after the open datatime')
                }
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(RegistrationForm, self).save(*args, **kwargs)


@receiver(post_save, sender=Event)
def create_registration_form(sender, instance, created, **kwargs):
    """Create a registration form when an event is created."""
    if created:
        RegistrationForm.objects.create(event=instance)


#TODO: come up with a way to not have to manually put in the Event fields as modifying Event will impact this model.
class EventCSV(models.Model):
    """Model for which fields are included within an Event based CSV."""
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="event_csv"
    )
    file_name = models.CharField(null=False, blank=False, max_length=200)
    event_name = models.BooleanField(default=True)
    description = models.BooleanField(default=False)
    published_status = models.BooleanField(default=False)
    show_schedule = models.BooleanField(default=False)
    featured_status = models.BooleanField(default=False)
    registration_type = models.BooleanField(default=False)
    registration_link = models.BooleanField(default=False)
    start_datetime = models.BooleanField(default=False)
    end_datetime = models.BooleanField(default=False)
    accessible_online = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    locations = models.BooleanField(default=False)
    sponsors = models.BooleanField(default=False)
    organisers = models.BooleanField(default=False)
    series = models.BooleanField(default=False)
    is_catered = models.BooleanField(default=False)
    contact_email_address = models.BooleanField(default=False)
    event_staff = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    approved_applications_count = models.BooleanField(default=False)
    pending_applications_count = models.BooleanField(default=False)
    rejected_applications_count = models.BooleanField(default=False)
    withdrawn_applications_count = models.BooleanField(default=False)


#TODO: come up with a way to not have to manually put in the Event Application fields as modifying Event Application will impact this model.
class EventApplicationsCSV(models.Model):
    """Model for which fields are included within an Event Application based CSV."""
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="event_application_csv"
    )
    file_name = models.CharField(null=False, blank=False, max_length=200)
    event_name = models.BooleanField(default=True)
    submitted_datetime = models.BooleanField(default=False)
    updated_datetime = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    participant_type = models.BooleanField(default=False)
    staff_comments = models.BooleanField(default=False)
    participant_first_name = models.BooleanField(default=False)
    participant_last_name = models.BooleanField(default=False)
    representing = models.BooleanField(default=False)
    emergency_contact_first_name = models.BooleanField(default=False)
    emergency_contact_last_name = models.BooleanField(default=False)
    emergency_contact_relationship = models.BooleanField(default=False)
    emergency_contact_phone_number = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    bill_to = models.BooleanField(default=False)
    billing_physical_address = models.BooleanField(default=False)
    billing_email_address = models.BooleanField(default=False)
    admin_billing_comments = models.BooleanField(default=False)

