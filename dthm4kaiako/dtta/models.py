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


class NewsArticle(models.Model):
    """Model for a news article published by DTTA."""

    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    content = RichTextUploadingField()
