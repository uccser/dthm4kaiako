"""Models for user application."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from utils.get_upload_filepath import get_entity_upload_path


class DietaryRequirement(models.Model):
    """Model for a dietary requirement e.g. vegetarian."""
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        """Text representation of a dietary requirement."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]
        verbose_name_plural = 'dietary requirements'

# TODO: remove school and city and add in school into Address model?
class User(AbstractUser):
    """User of website."""

    username = models.CharField(max_length=12, default='user')
    first_name = models.CharField(max_length=50, verbose_name='first name')
    last_name = models.CharField(max_length=150, verbose_name='last name')
    dietary_requirements = models.ManyToManyField(DietaryRequirement, related_name='users', blank=True, default='None')
    school = models.CharField(max_length=200, verbose_name='workplace', default='')
    city = models.CharField(max_length=150, verbose_name='city', default='')
    cell_phone_number = models.CharField(max_length=30, verbose_name='cell phone number', default='')
    medical_notes = models.TextField(default='')

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name']

    def get_absolute_url(self):
        """Return URL for user's webpage."""
        return reverse('users:detail', kwargs={'pk': self.pk})

    def __str__(self):
        """Name of the user."""
        return self.first_name


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

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]
        verbose_name_plural = 'entities'
