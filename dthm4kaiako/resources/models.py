"""Models for resources application."""

from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Resource(models.Model):
    """Model for a resource."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("resources:resource", kwargs={"pk": self.pk})

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of resource (str).
        """
        return self.name
