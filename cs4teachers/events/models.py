"""Models for the events application."""

from django.db import models
from django.utils.text import slugify

class Event(models.Model):
    """Model for event in database."""

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)

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


class Session(models.Model):
    """Model for session of event."""

    slug = models.SlugField(unique=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        """Text representation of Session object.

        Returns:
            Name of session (str).
        """
        return self.name


class Location(models.Model):
    """Model for location of session."""

    slug = models.SlugField(unique=True)
    event = models.ManyToManyField(
        Session,
        related_name="locations"
    )
    name = models.CharField(max_length=300)
    description = models.TextField(null=True)
    address = models.TextField()

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
