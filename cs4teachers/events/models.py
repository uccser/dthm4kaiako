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
