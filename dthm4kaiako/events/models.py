"""Models for resources application."""

import logging
from django.db import models
from utils.get_upload_filepath import (
    get_event_organiser_upload_path,
    get_event_sponsor_upload_path,
)
from ckeditor_uploader.fields import RichTextUploadingField


class Location(models.Model):
    """Model for a physical location."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    # TODO: Add geolocation fields


class Organiser(models.Model):
    """Model for an event organiser."""

    name = models.CharField(max_length=100)
    url = models.URLField(blank='')
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_organiser_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )


class Sponsor(models.Model):
    """Model for an event sponsor."""

    name = models.CharField(max_length=100)
    url = models.URLField(blank='')
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_sponsor_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )


class Event(models.Model):
    """Model for an event."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    registration_link = models.URLField(blank='')
    published = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        """Text representation of an event."""
        return self.name
