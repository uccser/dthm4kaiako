"""Models for POET application."""

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class ProgressOutcome(models.Model):
    """Model for an progress outcome."""

    progress_outcome_number = models.PositiveSmallIntegerField(default=1)
    code = models.CharField(max_length=30)
    label = models.CharField(max_length=30)
    short_label = models.CharField(max_length=10)
    learning_area = models.CharField(max_length=100)
    learning_area_code = models.CharField(max_length=10)
    technological_area = models.CharField(max_length=100)
    technological_area_code = models.CharField(max_length=10)
    content = models.TextField()

    def __str__(self):
        """Text representation of object.

        Returns:
            Code of progress outcome (str).
        """
        return self.label

    class Meta:
        """Meta options for class."""

        ordering = ['label', ]


class ProgressOutcomeGroup(models.Model):
    """Model for a group of progress outcomes in POET."""

    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    progress_outcomes = models.ManyToManyField(
        ProgressOutcome,
        related_name='groups',
        blank=True,
    )

    def __str__(self):
        """Text representation of object.

        Returns:
            Name of progress outcome group (str).
        """
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]


class Resource(models.Model):
    """Model for resource in POET."""

    title = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    target_progress_outcome = models.ForeignKey(
        ProgressOutcome,
        on_delete=models.CASCADE,
        related_name='resources',
    )
    content = RichTextUploadingField()

    def __str__(self):
        """Text representation of object.

        Returns:
            Code of resource (str).
        """
        return self.title


class Submission(models.Model):
    """Model for a resource in a form submission."""

    datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    feedback = models.TextField()
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    progress_outcome = models.ForeignKey(
        ProgressOutcome,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
