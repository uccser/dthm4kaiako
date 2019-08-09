"""Module for admin configuration for POET application."""

from django.contrib import admin
from poet.models import (
    ProgressOutcomeGroup,
    Resource,
    Submission,
)


class ProgressOutcomeGroupAdmin(admin.ModelAdmin):
    """Admin view for progress outcome group objects."""

    model = ProgressOutcomeGroup
    list_display = ('name', 'active')


class ResourceAdmin(admin.ModelAdmin):
    """Admin view for resource objects."""

    model = Resource
    list_display = ('title', 'target_progress_outcome', 'pk', 'active')


class SubmissionAdmin(admin.ModelAdmin):
    """Admin view for submission objects."""

    readonly_fields = ('datetime', )
    list_display = ('__str__', 'resource', 'progress_outcome', 'datetime')


admin.site.register(ProgressOutcomeGroup, ProgressOutcomeGroupAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Submission, SubmissionAdmin)
