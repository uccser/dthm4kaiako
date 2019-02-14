"""Models for resources application."""

from os.path import join, basename, splitext
from re import match
import logging
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
import filetype
from utils.get_upload_filepath import get_resource_upload_path
from utils.google_drive_api import get_google_drive_mimetype
from ckeditor_uploader.fields import RichTextUploadingField

ICON_PATH = 'img/icons/'
GOOGLE_DRIVE_REGEX = 'https://(drive|docs).google.com'
logger = logging.getLogger(__name__)


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
    TYPE_PDF = 11
    TYPE_IMAGE = 20
    TYPE_SLIDESHOW = 30
    TYPE_VIDEO = 40
    TYPE_WEBSITE = 50
    TYPE_AUDIO = 60
    TYPE_ARCHIVE = 70
    TYPE_RESOURCE = 80
    TYPE_SPREADSHEET = 90
    COMPONENT_TYPE_DATA = {
        TYPE_OTHER: {
            'icon': 'icons8-file-100.png',
            'text': _('Other'),
        },
        TYPE_DOCUMENT: {
            'icon': 'icons8-document-100.png',
            'text': _('Document'),
            'extensions': {
                'doc',
                'docx',
                'odt',
                'rtf',
                'tex',
                'txt',
                'wpd',
                'wks',
                'wps',
                'md',
                'markdown',
                'rst',
                'epub',
            },
            'mimetypes': {
                'application/vnd.google-apps.document',
            },
        },
        TYPE_PDF: {
            'icon': 'icons8-pdf-100.png',
            'text': _('PDF'),
            'extensions': {
                'pdf',
            }
        },
        TYPE_SPREADSHEET: {
            'icon': 'icons8-file-spreadsheet-100.png',
            'text': _('Spreadsheet'),
            'extensions': {
                'xlr',
                'xls',
                'xlsx',
                'ods',
            },
            'mimetypes': {
                'application/vnd.google-apps.spreadsheet',
            },
        },
        TYPE_IMAGE: {
            'icon': 'icons8-image-file-100.png',
            'text': _('Image'),
            'mimetypes': {
                'application/vnd.google-apps.drawing',
                'application/vnd.google-apps.photo',
            },
        },
        TYPE_SLIDESHOW: {
            'icon': 'icons8-image-file-100.png',
            'text': _('Slideshow'),
            'mimetypes': {
                'application/vnd.google-apps.presentation',
            },
        },
        TYPE_VIDEO: {
            'icon': 'icons8-video-file-100.png',
            'text': _('Video'),
            'url_regexes': {
                '^(http(s)?://)?((w){3}.)?youtu(be|.be)?(.com)?/.+',
                '^(http(s)?://)?((w){3}.|player.)?vimeo(.com)?/.+',
            },
            'mimetypes': {
                'application/vnd.google-apps.video',
            },
        },
        TYPE_WEBSITE: {
            'icon': 'icons8-website-100.png',
            'text': _('Website'),
        },
        TYPE_AUDIO: {
            'icon': 'icons8-audio-file-100.png',
            'text': _('Audio'),
        },
        TYPE_ARCHIVE: {
            'icon': 'icons8-zipped-file-100.png',
            'text': _('Archive'),
        },
        TYPE_RESOURCE: {
            'icon': 'icons8-versions-100.png',
            'text': _('Resource'),
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
            self.component_type = self.get_url_type()
        elif self.component_resource:
            self.component_type = self.TYPE_RESOURCE
        else:
            self.component_type = self.get_file_type()
        logging.info('Component {} detected as type {}'.format(self.name, self.component_type))
        super().save(*args, **kwargs)

    def get_url_type(self):
        """Determine type of URL.

        For example, a YouTube URL should be labeled as video type.
        """
        # If Google Drive
        if match(GOOGLE_DRIVE_REGEX, self.component_url):
            logger.info('Google Drive URL detected: {}'.format(self.component_url))
            url_mimetype = get_google_drive_mimetype(self.component_url)
            logger.info('Detected Google Drive mimeType: {}'.format(url_mimetype))
            for type_code, type_data in self.COMPONENT_TYPE_DATA.items():
                if url_mimetype in type_data.get('mimetypes', set()):
                    return type_code
            return self.TYPE_OTHER
        else:
            for type_code, type_data in self.COMPONENT_TYPE_DATA.items():
                for regex in type_data.get('url_regexes', set()):
                    if match(regex, self.component_url):
                        return type_code
            return self.TYPE_WEBSITE

    def get_file_type(self):
        """Determine type of file.

        Check extension before bytes, to correctly identify documents
        and PDF files. All other types are detected by bytes.
        """
        extension = splitext(self.component_file.name)[1][1:]
        for type_code, type_data in self.COMPONENT_TYPE_DATA.items():
            if extension in type_data.get('extensions', set()):
                return type_code

        file_obj = self.component_file.open()
        if filetype.image(file_obj):
            return self.TYPE_IMAGE
        elif filetype.video(file_obj):
            return self.TYPE_VIDEO
        elif filetype.audio(file_obj):
            return self.TYPE_AUDIO
        elif filetype.archive(file_obj):
            return self.TYPE_ARCHIVE
        else:
            return self.TYPE_OTHER

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
        if self.component_resource == self.resource:
            raise ValidationError(_('Cannot set a resource to be a component of itself.'))

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of resource component (str).
        """
        return self.name
