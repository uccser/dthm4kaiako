"""Models for DTTA application."""

from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from utils.get_upload_filepath import get_dtta_news_article_source_upload_path


class Page(models.Model):
    """Model for a flat page on DTTA website."""

    PAGE_PLANNING = 1
    PAGE_DOCUMENT = 2
    PAGE_ABOUT = 3
    PAGE_MEMBERSHIP = 4
    PAGE_CHOICES = (
        (PAGE_PLANNING, 'Planning'),
        (PAGE_DOCUMENT, 'Documents'),
        (PAGE_ABOUT, 'About'),
        (PAGE_MEMBERSHIP, 'Membership'),
    )

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', always_update=True, null=True)
    date = models.DateField()
    page_type = models.PositiveSmallIntegerField(
        choices=PAGE_CHOICES,
        default=PAGE_PLANNING,
    )
    order_number = models.PositiveSmallIntegerField(default=1)
    published = models.BooleanField(default=False)
    content = HTMLField()

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


class Project(models.Model):
    """Model for a flat page of a project on the DTTA website.

    TODO: Combine Page and Project models.
    """

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', always_update=True, null=True)
    date = models.DateField()
    order_number = models.PositiveSmallIntegerField(default=1)
    published = models.BooleanField(default=False)
    content = HTMLField()

    def get_absolute_url(self):
        """Return URL of object on website.

        Returns:
            URL as a string.
        """
        return reverse("dtta:project", kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of DTTA project page (str).
        """
        return self.title


class NewsArticleAudience(models.Model):
    """Model for an audience of a news article published by DTTA."""

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)
    colour = models.CharField(
        max_length=20,
        help_text=(
            "Available colours: 'red', 'pink', 'orange', 'yellow', 'green',"
            "'teal', 'cyan', 'blue', 'indigo', 'purple', 'gray', 'gray-dark'."
        )
    )

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of news article audience (str).
        """
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name']


class NewsArticleSource(models.Model):
    """Model for a source of a news article published by DTTA."""

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_dtta_news_article_source_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )
    website = models.URLField(blank=True)

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of news article source (str).
        """
        return self.name

    def save(self, *args, **kwargs):
        """Override save method to ensure logo is saved to correct directory.

        The method saves the file once the instance has a primary key,
        as the upload_to function of the file uses this key.

        This method is adapted from the answer at:
        https://stackoverflow.com/a/58853713/10345299
        """
        if self.pk is None:
            saved_image = self.logo
            self.logo = None
            super().save(*args, **kwargs)
            self.logo = saved_image
            kwargs.pop('force_insert', None)
        super().save(*args, **kwargs)


class NewsArticle(models.Model):
    """Model for a news article published by DTTA."""

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', always_update=True, null=True)
    datetime = models.DateTimeField()
    content = HTMLField()
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
