"""Models for DTTA application."""

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Page(models.Model):
    """Model for a flat page on DTTA website."""

    title = models.CharField(max_length=200)
    date = models.DateField()
    order_number = models.PositiveSmallIntegerField(default=1)
    published = models.BooleanField(default=False)
    content = RichTextUploadingField()

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of DTTA page (str).
        """
        return self.title


class NewsArticle(models.Model):
    """Model for a news article published by DTTA."""

    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    content = RichTextUploadingField()

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of news article (str).
        """
        return self.title


class RelatedLink(models.Model):
    """Model for a related link for DTTA homepage."""

    name = models.CharField(max_length=200)
    url = models.URLField()
    order_number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of related link (str).
        """
        return self.name
