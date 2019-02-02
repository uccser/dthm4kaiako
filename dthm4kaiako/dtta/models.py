"""Models for DTTA application."""

from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from utils.get_upload_filepath import get_dtta_news_article_source_upload_path


class Page(models.Model):
    """Model for a flat page on DTTA wresourceebsite."""

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', always_update=True, null=True)
    date = models.DateField()
    order_number = models.PositiveSmallIntegerField(default=1)
    published = models.BooleanField(default=False)
    content = RichTextUploadingField()

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("dtta:page", kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of DTTA page (str).
        """
        return self.title


class NewsArticleAudience(models.Model):
    """Model for an audience of a news article published by DTTA."""

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)
    colour = models.CharField(max_length=20)

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of news article audience (str).
        """
        return self.name


class NewsArticleSource(models.Model):
    """Model for a source of a news article published by DTTA."""

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)
    logo = models.ImageField(null=True, blank=True, upload_to=get_dtta_news_article_source_upload_path)
    website = models.URLField(blank=True)

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of news article source (str).
        """
        return self.name


class NewsArticle(models.Model):
    """Model for a news article published by DTTA."""

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', always_update=True, null=True)
    datetime = models.DateTimeField()
    content = RichTextUploadingField()
    source = models.ForeignKey(
        NewsArticleSource,
        on_delete=models.CASCADE,
        related_name='news_articles',
        null=True,
        blank=True,
    )
    audiences = models.ManyToManyField(
        NewsArticleAudience,
        related_name='news_articles',
        blank=True,
    )

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("dtta:news_article", kwargs={'pk': self.pk, 'slug': self.slug})

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
