"""Module for admin configuration for the resources application."""

from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from resources.models import (
    Resource,
    ResourceComponent,
    Language,
    TechnologicalArea,
    ProgressOutcome,
    NZQAStandard,
    YearLevel,
    CurriculumLearningArea,
)


class NZQAStandardAdmin(admin.ModelAdmin):
    """Configuration for displaying NZQA Standards in admin."""

    list_display = (
        'level',
        'abbreviation',
        'name',
        'credit_value',
        'standard_type'
    )
    ordering = ('level', 'abbreviation')


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


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = '__all__'

    def clean(self):
        """Validate form values.

        Raises:
            ValidationError if invalid values.
        """
        # Check at least one author exists
        if self.cleaned_data['author_entities'].count() + self.cleaned_data['author_users'].count() == 0:
            raise forms.ValidationError(_('At least one author (entity or user) must be listed.'))


class ResourceAdmin(admin.ModelAdmin):
    """Admin view for resource objects."""

    form = ResourceForm
    inlines = [ResourceComponentInline]
    list_display = (
        'name',
        'datetime_added',
        'datetime_updated',
        'published',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'description',
                )
            }
        ),
        ('Metadata', {
            'fields': (
                'languages',
                'technological_areas',
                'progress_outcomes',
                'nzqa_standards',
                'year_levels',
                'curriculum_learning_areas',
            ),
        }),
        ('Ownership', {
            'description': 'Resources can be owned by both users and entities.',
            'fields': (
                'author_entities',
                'author_users',
            ),
        }),
        ('Visibility', {
            'fields': (
                'published',
            ),
        }),
    )
    filter_horizontal = (
        'languages',
        'technological_areas',
        'progress_outcomes',
        'nzqa_standards',
        'year_levels',
        'curriculum_learning_areas',
        'author_entities',
        'author_users',
    )

    class Media:
        """Custom media file overrides."""

        css = {
            'all': ('css/admin-overrides.css', )
        }


admin.site.register(Language)
admin.site.register(TechnologicalArea)
admin.site.register(ProgressOutcome)
admin.site.register(NZQAStandard, NZQAStandardAdmin)
admin.site.register(YearLevel)
admin.site.register(CurriculumLearningArea)
admin.site.register(Resource, ResourceAdmin)
