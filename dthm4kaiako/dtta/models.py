"""Models for DTTA application."""

from django.db import models
from markdownx.models import MarkdownxField


class NewsArticle(models.Model):
    """Model for a news article published by DTTA."""

    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    content = MarkdownxField()
