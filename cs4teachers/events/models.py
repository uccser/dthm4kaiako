"""Models for the events application."""

from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django_google_maps import fields as map_fields


class Location(models.Model):
    """Model for location of session."""

    slug = AutoSlugField(unique=True, populate_from="name")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("events:location", kwargs={"location_slug": self.slug})

    def __str__(self):
        """Text representation of Location object.

        Returns:
            Name of location (str).
        """
        return self.name


class LocationImage(models.Model):
    """Model for image of location model."""

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/locations/")
    location = models.ForeignKey(
        Location,
        related_name="images",
    )

    def __str__(self):
        """Text representation of LocationImage object.

        Returns:
            Name of image (str).
        """
        return self.name


class Series(models.Model):
    """Model for event series."""

    slug = AutoSlugField(unique=True, populate_from="name")
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="images/series/", null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        """Text representation of Series object.

        Returns:
            Name of series (str).
        """
        return self.name


class Sponsor(models.Model):
    """Model for sponsor of event."""

    name = models.CharField(max_length=200)
    url = models.URLField()
    logo = models.ImageField(upload_to="images/sponsors/", null=True, blank=True)

    def __str__(self):
        """Text representation of Sponsor object.

        Returns:
            Name of sponsor (str).
        """
        return self.name


class EventBase(models.Model):
    """Abstract base class for event models."""

    slug = AutoSlugField(unique=True, populate_from="name")
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)

    class Meta:
        """Meta attributes of the class."""

        abstract = True


class Event(EventBase):
    """Model for event in database."""

    location = models.ForeignKey(
        Location,
        related_name="events",
        null=True,
    )
    series = models.ForeignKey(
        Series,
        related_name="events",
        null=True,
        blank=True,
    )
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name="events",
        blank=True,
    )

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("events:event", kwargs={"event_slug": self.slug})

    def __str__(self):
        """Text representation of Event object.

        Returns:
            Name of event (str).
        """
        if self.series:
            return "{}: {}".format(self.series.name, self.name)
        else:
            return self.name


class EventImage(models.Model):
    """Model for image of event model."""

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/events/")
    location = models.ForeignKey(
        Event,
        related_name="images",
    )

    def __str__(self):
        """Text representation of EventImage object.

        Returns:
            Name of image (str).
        """
        return self.name


class Resource(models.Model):
    """Model for resource used in sessions."""

    slug = AutoSlugField(unique=True, populate_from="name")
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/resources/", null=True, blank=True)

    def __str__(self):
        """Text representation of Resource object.

        Returns:
            Name of resource (str).
        """
        return self.name


class Session(models.Model):
    """Model for session of event."""

    slug = AutoSlugField(unique_with=["event__slug"], populate_from="name")
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/sessions/", null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    locations = models.ManyToManyField(
        Location,
        related_name="sessions",
        blank=True,
    )
    resources = models.ManyToManyField(
        Resource,
        related_name="sessions",
        blank=True,
    )

    def __str__(self):
        """Text representation of Session object.

        Returns:
            Name of session (str).
        """
        return self.name


class ThirdPartyEvent(EventBase):
    """Model for third party event in database."""

    url = models.URLField()
    location = models.ForeignKey(
        Location,
        related_name="third_party_events",
        null=True,
    )

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("events:third_party_event", kwargs={"event_slug": self.slug})

    def __str__(self):
        """Text representation of Event object.

        Returns:
            Name of event (str).
        """
        return self.name
