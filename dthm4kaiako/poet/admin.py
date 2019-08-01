"""Module for admin configuration for POET application."""

from django.contrib import admin
from poet.models import (
    ProgressOutcomeGroup,
    Resource,
    Submission,
)


class ResourceAdmin(admin.ModelAdmin):
    """Admin view for resource objects."""

    model = Resource
    list_display = ('title', 'target_progress_outcome', 'pk', 'active')


class SubmissionAdmin(admin.ModelAdmin):
    """Admin view for submission objects."""

    readonly_fields = ('datetime', )
    list_display = ('__str__', 'resource', 'progress_outcome', 'datetime')


admin.site.register(ProgressOutcomeGroup)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Submission, SubmissionAdmin)
