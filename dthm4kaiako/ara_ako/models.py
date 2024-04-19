"""Models for Ara Ako application."""

from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from events.models import Event
from resources.models import Resource


class AraAkoEvent(models.Model):
    """Model for an Ara Ako event."""

    slug = models.SlugField()
    published = models.BooleanField(default=False)
    event = models.OneToOneField(
        Event,
        verbose_name='Event',
        related_name='ara_ako_event',
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        """Return URL of Ara Ako event on website.

        Returns:
            URL as a string.
        """
        return reverse('ara_ako:event', kwargs={'slug': self.slug})

    def __str__(self):
        """Text representation of an Ara Ako event."""
        return self.event.name

    class Meta:
        """Meta options for class."""

        ordering = ['-event__start', ]


class AraAkoTeam(models.Model):
    """Model for an Ara Ako team."""

    number = models.PositiveSmallIntegerField()
    description = HTMLField()
    resource = models.OneToOneField(
        Resource,
        verbose_name='Ara Ako team resource',
        related_name='ara_ako_team',
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey(
        AraAkoEvent,
        verbose_name='Ara Ako teams',
        related_name='teams',
        on_delete=models.CASCADE,
    )
