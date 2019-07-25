"""Models for POET application."""

from django.db import models
from utils.get_upload_filepath import get_poet_resource_upload_path


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


class Resource(models.Model):
    """Model for resource in POET."""

    title = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    target_progress_outcome = models.ForeignKey(
        ProgressOutcome,
        on_delete=models.CASCADE,
        related_name='resources',
    )
    pdf = models.FileField(
        upload_to=get_poet_resource_upload_path,
    )

    def __str__(self):
        """Text representation of object.

        Returns:
            Code of resource (str).
        """
        return self.title


class Submission(models.Model):
    """"""
    datetime = models.DateTimeField(auto_now_add=True)
    # TODO: IP address for anti cheating
    # TODO: Time taken for anti cheating
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
