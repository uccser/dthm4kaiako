"""Models for get started application."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from resources.models import Resource


class Component(models.Model):
    """Model for an get started component."""

    order_number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True, null=True)
    description = HTMLField()
    video_url = models.URLField(blank=True)
    video_transcript = HTMLField(blank=True)
    # Visibility
    VISIBILITY_HIDDEN = 1
    VISIBILITY_COMING_SOON = 2
    VISIBILITY_PUBLISHED = 3
    VISIBILITY_CHOICES = (
        (VISIBILITY_HIDDEN, _('Hidden')),
        (VISIBILITY_COMING_SOON, _('Coming soon')),
        (VISIBILITY_PUBLISHED, _('Published')),
    )
    visibility = models.PositiveSmallIntegerField(
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_HIDDEN,
    )
    resource = models.OneToOneField(
        Resource,
        verbose_name='resource',
        related_name='get_started_component',
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        """Text representation of a get started component."""
        return self.name

    def get_absolute_url(self):
        """Return URL of component.

        Returns:
            URL as a string.
        """
        return reverse('get_started:component', kwargs={'slug': self.slug})

    class Meta:
        """Meta options for class."""

        ordering = ['order_number', ]
