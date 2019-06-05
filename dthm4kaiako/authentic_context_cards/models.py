"""Models for authentic context cards application."""

from django.db import models


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


class ProgressOutcome(models.Model):
    """Model for an progress outcome."""

    progress_outcome_number = models.PositiveSmallIntegerField(default=1)
    code = models.CharField(max_length=30)
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
        return self.code
