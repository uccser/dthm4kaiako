"""Models for DTTA application."""

from django.db import models
from martor.models import MartorField


class NewsArticle(models.Model):
    """Model for a news article published by DTTA."""

    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    content = MartorField()
