"""Module for admin configuration for the resources application."""

from django.contrib import admin
from resources.models import (
    Resource,
    ResourceComponent,
    Language,
    CurriculumStrand,
    ProgressOutcome,
    NZQAStandard,
    YearLevel,
    CurriculumLearningArea,
)


class ResourceComponentInline(admin.StackedInline):
    """Inline view for resource component objects."""

    model = ResourceComponent
    fk_name = 'resource'
    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        ('Item', {
            'fields': ('component_url', 'component_file', 'component_resource'),
            'description': 'Only one of the following fields must be filled for each component.'
        }),
    )


class ResourceAdmin(admin.ModelAdmin):
    """Admin view for resource objects."""

    model = Resource
    inlines = [ResourceComponentInline]

admin.site.register(Language)
admin.site.register(CurriculumStrand)
admin.site.register(ProgressOutcome)
admin.site.register(NZQAStandard)
admin.site.register(YearLevel)
admin.site.register(CurriculumLearningArea)
admin.site.register(Resource, ResourceAdmin)
