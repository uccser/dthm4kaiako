"""Models for user application."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """User of website."""

    username = models.CharField(max_length=6, null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name="first name")
    last_name = models.CharField(max_length=150, verbose_name="last name")

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name']

    def get_absolute_url(self):
        """Return URL for user's webpage."""
        return reverse("users:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.first_name
