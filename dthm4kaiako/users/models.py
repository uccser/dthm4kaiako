"""Models for user application."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from utils.get_upload_filepath import get_entity_upload_path


class User(AbstractUser):
    """User of website."""

    username = models.CharField(max_length=12, default='user')
    first_name = models.CharField(max_length=50, verbose_name='first name')
    last_name = models.CharField(max_length=150, verbose_name='last name')

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name']

    def get_absolute_url(self):
        """Return URL for user's webpage."""
        return reverse('users:detail', kwargs={'pk': self.pk})

    def __str__(self):
        """Name of the user."""
        return self.first_name


class DietaryRequirement(models.Model):
    """Model for a dietary requirement e.g. vegetarian."""
    name = models.CharField(max_length=20)
    users = model.ManyToManyField(User)

    def __str__(self):
        """Text representation of a dietary requirement."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]
        verbose_name_plural = 'dietary requirements'


class Entity(models.Model):
    """Model for an entity (organisation, company, group, etc)."""

    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True)
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_entity_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )

    def __str__(self):
        """Text representation of a entity."""
        return self.name

    def save(self, *args, **kwargs):
        """Override default save method.

        Establishes object to use pk in saving logo image.
        """
        if self.pk is None:
            saved_logo = self.logo
            self.logo = None
            super(Entity, self).save(*args, **kwargs)
            self.logo = saved_logo
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super(Entity, self).save(*args, **kwargs)

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]
        verbose_name_plural = 'entities'
