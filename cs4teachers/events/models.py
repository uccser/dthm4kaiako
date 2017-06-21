"""Models for the events application."""

from django.db import models
from django.utils.text import slugify

class Event(models.Model):
    """Model for event in database."""

    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    is_published = models.BooleanField(default=False)

    def start_datetime(self):
        return self.sessions.earliest("start_datetime").start_datetime

    def end_datetime(self):
        return self.sessions.latest("end_datetime").end_datetime

    def save(self, *args, **kwargs):
        """Set slug of object as name upon creation."""
        if not self.id:
            self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        """Text representation of Event object.

        Returns:
            Name of event (str).
        """
        return self.name


class Location(models.Model):
    """Model for location of session."""

    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = models.TextField()

    def save(self, *args, **kwargs):
        """Set slug of object as name upon creation."""
        if not self.id:
            self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

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


class Resource(models.Model):
    """Model for resource used in sessions."""
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """Set slug of object as name upon creation."""
        if not self.id:
            self.slug = slugify(self.name)
        super(Resource, self).save(*args, **kwargs)

    def __str__(self):
        """Text representation of Resource object.

        Returns:
            Name of resource (str).
        """
        return self.name


class Session(models.Model):
    """Model for session of event."""

    slug = models.SlugField(max_length=200)
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

    def save(self, *args, **kwargs):
        """Set slug of object as name upon creation."""
        if not self.id:
            self.slug = slugify(self.name)
        super(Session, self).save(*args, **kwargs)

    def __str__(self):
        """Text representation of Session object.

        Returns:
            Name of session (str).
        """
        return self.name

    class Meta:
        unique_together = ("event", "slug",)
