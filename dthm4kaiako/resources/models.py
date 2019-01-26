"""Models for resources application."""

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from utils.get_upload_filepath import get_resource_upload_path
from ckeditor_uploader.fields import RichTextUploadingField


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
    DATA_FIELDS = ['url', 'file_obj', 'image']
    TYPE_OTHER = 0
    TYPE_DOCUMENT = 10
    TYPE_IMAGE = 20
    TYPE_SLIDESHOW = 30
    TYPE_VIDEO = 40
    TYPE_WEBSITE = 50
    COMPONENT_TYPE_CHOICES = (
        (TYPE_OTHER, _('Other')),
        (TYPE_DOCUMENT, _('Document')),
        (TYPE_IMAGE, _('Image')),
        (TYPE_SLIDESHOW, _('Slideshow')),
        (TYPE_VIDEO, _('Video')),
        (TYPE_WEBSITE, _('Website')),
    )

    # Attributes
    name = models.CharField(max_length=300)
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='components',
    )
    url = models.URLField(blank=True)
    file_obj = models.FileField(null=True, blank=True, upload_to=get_resource_upload_path)
    image = models.ImageField(null=True, blank=True, upload_to=get_resource_upload_path)
    component_type = models.PositiveSmallIntegerField(
        choices=COMPONENT_TYPE_CHOICES,
        default=TYPE_OTHER,
    )

    def save(self, *args, **kwargs):
        """Determine the value for 'component_type', then save object."""
        if self.url:
            self.component_type = self.TYPE_WEBSITE
        elif self.image:
            self.component_type = self.TYPE_IMAGE
        super().save(*args, **kwargs)

    def clean(self):
        """Only allow one type of data in a resource component."""
        data_count = 0
        for field in self.DATA_FIELDS:
            print(getattr(self, field, None), bool(getattr(self, field, None)))
            if getattr(self, field, None):
                data_count += 1
        print(data_count)
        if data_count != 1:
            raise ValidationError(_('Resource components must have exactly one type of data (file, URL, image, etc).'))

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of resource component (str).
        """
        return self.name
