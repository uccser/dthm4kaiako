"""Models for resources application."""

from os.path import join, basename
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
import filetype
from utils.get_upload_filepath import get_resource_upload_path
from ckeditor_uploader.fields import RichTextUploadingField

ICON_PATH = 'img/icons/'


class Resource(models.Model):
    """Model for a resource."""

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True, null=True)
    description = RichTextUploadingField()
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("resources:resource", kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of resource (str).
        """
        return self.name


class ResourceComponent(models.Model):
    """Model for a resource component."""

    # Constants
    DATA_FIELDS = [
        'component_url',
        'component_file',
        'component_resource',
    ]
    TYPE_OTHER = 0
    TYPE_DOCUMENT = 10
    TYPE_IMAGE = 20
    TYPE_SLIDESHOW = 30
    TYPE_VIDEO = 40
    TYPE_WEBSITE = 50
    TYPE_AUDIO = 60
    TYPE_ARCHIVE = 70
    TYPE_RESOURCE = 80
    COMPONENT_TYPE_DATA = {
        TYPE_OTHER: {
            "icon": "icons8-file-100.png",
            "text": _('Other'),
        },
        TYPE_DOCUMENT: {
            "icon": "icons8-document-100.png",
            "text": _('Document'),
        },
        TYPE_IMAGE: {
            "icon": "icons8-image-file-100.png",
            "text": _('Image'),
        },
        TYPE_SLIDESHOW: {
            "icon": "icons8-image-file-100.png",
            "text": _('Slideshow'),
        },
        TYPE_VIDEO: {
            "icon": "icons8-video-file-100.png",
            "text": _('Video'),
        },
        TYPE_WEBSITE: {
            "icon": "icons8-website-100.png",
            "text": _('Website'),
        },
        TYPE_AUDIO: {
            "icon": "icons8-audio-file-100.png",
            "text": _('Audio'),
        },
        TYPE_ARCHIVE: {
            "icon": "icons8-zipped-file-100.png",
            "text": _('Archive'),
        },
        TYPE_RESOURCE: {
            "icon": "icons8-versions-100.png",
            "text": _('Resource'),
        },
    }
    choices = []
    for type_value, type_data in COMPONENT_TYPE_DATA.items():
        choices.append((type_value, type_data['text']))
    COMPONENT_TYPE_CHOICES = tuple(choices)

    # Attributes - General
    name = models.CharField(max_length=300)
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='components',
    )
    component_type = models.PositiveSmallIntegerField(
        choices=COMPONENT_TYPE_CHOICES,
        default=TYPE_OTHER,
    )
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    # Attributes - Components (only 1 can be filled)
    component_url = models.URLField(blank=True)
    component_file = models.FileField(null=True, blank=True, upload_to=get_resource_upload_path)
    component_resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='component_of',
        blank=True,
        null=True,
    )

    def icon_path(self):
        """Return path for icon for component type.

        Returns:
            String of path to icon file.
        """
        return join(ICON_PATH, self.COMPONENT_TYPE_DATA[self.component_type]['icon'])

    def filename(self):
        """Return filename of file component.

        Returns:
            Filename of file component as string, otherwise None.
        """
        filename = None
        if self.component_file:
            filename = basename(self.component_file.name)
        return filename

    def save(self, *args, **kwargs):
        """Determine the value for 'component_type', then save object."""
        if self.component_url:
            # TODO: If website is image or video, apply label appropriately.
            self.component_type = self.TYPE_WEBSITE
        elif self.component_resource:
            self.component_type = self.TYPE_RESOURCE
        elif filetype.image(self.component_file):
            self.component_type = self.TYPE_IMAGE
        elif filetype.video(self.component_file):
            self.component_type = self.TYPE_VIDEO
        elif filetype.audio(self.component_file):
            self.component_type = self.TYPE_AUDIO
        elif filetype.archive(self.component_file):
            # TODO: Move PDF detection to document type.
            self.component_type = self.TYPE_ARCHIVE
        # TODO: Check for document types, possibly by extension.
        else:
            self.component_type = self.TYPE_OTHER
        super().save(*args, **kwargs)

    def clean(self):
        """Only allow one type of data in a resource component."""
        data_count = 0
        for field in self.DATA_FIELDS:
            if getattr(self, field, None):
                data_count += 1
        if data_count != 1:
            raise ValidationError(
                _('Resource components must have exactly one type of data (file, URL, or another resource).')
                )
        # TODO: Resource cannot be a component of itself.

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of resource component (str).
        """
        return self.name
