"""Models for authentic context cards application."""

from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from utils.get_upload_filepath import get_dtta_news_article_source_upload_path


class AchievementObjective(models.Model):
    """Model for an achievement objective."""

    code = models.CharField(max_length=30)
    learning_area = models.CharField(max_length=100)
    learning_area_code = models.CharField(max_length=10)
    level = models.PositiveSmallIntegerField(default=1)
    component = models.CharField(max_length=100)
    component_code = models.CharField(max_length=10)
    strand = models.CharField(max_length=100)
    strand_code = models.CharField(max_length=10)
    content = models.TextField()

    def __str__(self):
        """Text representation of object.

        Returns:
            Code of acheivement objective (str).
        """
        return self.code
