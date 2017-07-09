"""Models for the events application."""

from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django_google_maps import fields as map_fields


class Location(models.Model):
    """Model for location of session."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def __str__(self):
        """Text representation of Location object.

        Returns:
            Name of location (str).
        """
        return self.name


class Sponsor(models.Model):
    """Model for sponsor of event."""

    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        """Text representation of Sponsor object.

        Returns:
            Name of sponsor (str).
        """
        return self.name


class EventBase(models.Model):
    """Abstract base class for event models."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=150)
    description = models.TextField()
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
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name="events",
    )

    def start_datetime(self):
        """Retrieve start datetime of event from earliest session.

        Returns:
            Datetime object of event start.
        """
        return self.sessions.earliest("start_datetime").start_datetime

    def end_datetime(self):
        """Retrieve end datetime of event from latest session.

        Returns:
            Datetime object of event end.
        """
        return self.sessions.latest("end_datetime").end_datetime

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
        return self.name


class Resource(models.Model):
    """Model for resource used in sessions."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        """Text representation of Resource object.

        Returns:
            Name of resource (str).
        """
        return self.name


class Session(models.Model):
    """Model for session of event."""

    slug = AutoSlugField(populate_from="name", unique_with=["event__slug"])
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
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
    start_date = models.DateField()
    end_date = models.DateField()
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
