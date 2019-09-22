"""Models for secret pages application."""

from django.db import models
from django.conf import settings
from django.template.loader import get_template, TemplateDoesNotExist
from django.core.exceptions import ValidationError

TEMPLATE_EXTENSION = '.html'


class SecretPage(models.Model):
    """Model for a secret page."""

    name = models.CharField(
        unique=True,
        max_length=150,
    )
    slug = models.SlugField(unique=True)
    template = models.CharField(
        max_length=300,
        help_text="File extension (.html) is not required."
    )
    active = models.BooleanField(default=False)

    def clean(self):
        """Check template exists and set to full path."""
        if self.template.endswith(TEMPLATE_EXTENSION):
            self.template = self.template[:-len(TEMPLATE_EXTENSION)]
        template_path = settings.SECRET_PAGES_TEMPLATE_TEMPLATE.format(self.template)
        try:
            get_template(template_path)
        except TemplateDoesNotExist:
            raise ValidationError('Template "{}" cannot be found.'.format(template_path))

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of secret page (str).
        """
        return self.name
