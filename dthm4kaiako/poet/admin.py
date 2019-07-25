"""Module for admin configuration for POET application."""

from django.contrib import admin
from poet.models import (
    ProgressOutcome,
    Resource,
    Submission,
)


class ResourceAdmin(admin.ModelAdmin):
    """Admin view for resource objects."""

    model = Resource
    list_display = ('title', 'target_progress_outcome', 'active')


admin.site.register(ProgressOutcome)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Submission)
