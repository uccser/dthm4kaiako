"""Module for admin configuration for POET application."""

from django.contrib import admin
from poet.models import (
    ProgressOutcome,
    Resource,
    Submission,
)

admin.site.register(ProgressOutcome)
admin.site.register(Resource)
admin.site.register(Submission)
