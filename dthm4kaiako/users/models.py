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
    # TODO: Change to own model. Should be Many to Many relationship
    # DIETARY_GLUTEN_FREE = 'GF'
    # DIETARY_DAIRY_FREE = 'DF'
    # DIETARY_VEGETARIAN = 'V'
    # DIETARY_VEGAN = 'VE'
    # DIETARY_HALAL = 'H'
    # DIETARY_KETO = 'K'
    # DIETARY_PALEO = 'P'
    # DIETARY_FODMAP = 'FM'
    # DIETARY_NUT_ALLERGY = 'N'
    # DIETARY_FISH_ALLERGY = 'FA'
    # DIETARY_NONE = 'NO'
    # DIETARY_CHOICES = (
    #     (DIETARY_GLUTEN_FREE, _('Gluten Free')),
    #     (DIETARY_DAIRY_FREE, _('Dairy Free')),
    #     (DIETARY_VEGETARIAN, _('Vegetarian')),
    #     (DIETARY_VEGAN, _('Vegan')),
    #     (DIETARY_HALAL, _('Halal')),
    #     (DIETARY_KETO, _('Keto')),
    #     (DIETARY_PALEO, _('Paleo')),
    #     (DIETARY_FODMAP, _('FODMAP')),
    #     (DIETARY_NUT_ALLERGY, _('Nut allergies')),
    #     (DIETARY_FISH_ALLERGY, _('Fish and shellfish allergies')),
    #     (DIETARY_NONE, _('None')),
    # )
    # dietary_requirements = models.CharField(
    #     max_length=2,
    #     choices = DIETARY_CHOICES,
    #     default=DIETARY_NONE,
    # )
    workplace = models.CharField(max_length=350, verbose_name='workplace', default='')
    city = models.CharField(max_length=150, verbose_name='city', default='')
    cell_phone_number = models.CharField(max_length=20, verbose_name='cell phone number', default='')
    medical_notes = models.TextField(verbose_name='medical notes', default='')
    event_applications = models.ForeignKey(
        'events.EventApplication',
        on_delete=models.CASCADE,
        related_name='user',
        null=True,
        blank=True,
    )
    billing_address = models.TextField(verbose_name='billing address', default='')

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


# class DietaryRequirement(models.Model):
#     """Model for a dietary requirement."""

#     name = models.CharField(max_length=100, unique=True)
