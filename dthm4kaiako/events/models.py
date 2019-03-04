"""Models for resources application."""

from django.db import models
from django.contrib.gis.db import models as geomodels
from utils.get_upload_filepath import (
    get_event_organiser_upload_path,
    get_event_sponsor_upload_path,
    get_event_series_upload_path,
)
from ckeditor_uploader.fields import RichTextUploadingField


class Location(models.Model):
    """Model for a physical location."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    coords = geomodels.PointField()

    def __str__(self):
        """Text representation of a name."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name']


class Organiser(models.Model):
    """Model for an event organiser."""

    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_organiser_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )

    def __str__(self):
        """Text representation of an event organiser."""
        return self.name


class Sponsor(models.Model):
    """Model for an event sponsor."""

    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_sponsor_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )

    def __str__(self):
        """Text representation of an sponsor."""
        return self.name


class Session(models.Model):
    """"Model for an event session."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    url = models.URLField(blank=True)
    url_label = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    locations = models.ManyToManyField(
        Location,
        related_name='sessions',
        blank=True,
    )

    def __str__(self):
        """Text representation of an session."""
        return self.name


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
    registration_link = models.URLField(blank=True)
    published = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    locations = models.ManyToManyField(
        Location,
        related_name='events',
        blank=True,
    )
    sessions = models.ManyToManyField(
        Session,
        related_name='events',
        blank=True,
    )
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name='events',
        blank=True,
    )
    organisers = models.ManyToManyField(
        Organiser,
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

    def __str__(self):
        """Text representation of an event."""
        return self.name
