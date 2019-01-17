from django.db import models
from markdownx.models import MarkdownxField


class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    content = MarkdownxField()
