"""Module for forms for resource module."""

from django import forms
from haystack.forms import FacetedSearchForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Layout, Submit, Row, Column
from resources.models import (
    Resource,
    Language,
    TechnologicalArea,
    ProgressOutcome,
    NZQAStandard,
    YearLevel,
    CurriculumLearningArea,
)


class ResourceSearchForm(FacetedSearchForm):
    """Class for resource search form."""

    lang = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=False,
        label='Languages',
        widget=forms.CheckboxSelectMultiple(),
    )
    tech_area = forms.ModelMultipleChoiceField(
        queryset=TechnologicalArea.objects.all(),
        required=False,
        label='Technological areas',
        widget=forms.CheckboxSelectMultiple(),
    )
    progress_outcome = forms.ModelMultipleChoiceField(
        queryset=ProgressOutcome.objects.all(),
        required=False,
        label='Progress outcomes',
        widget=forms.CheckboxSelectMultiple(),
    )
    nzqa_standard = forms.ModelMultipleChoiceField(
        queryset=NZQAStandard.objects.all(),
        required=False,
        label='NZQA standards',
        widget=forms.CheckboxSelectMultiple(),
    )
    year_level = forms.ModelMultipleChoiceField(
        queryset=YearLevel.objects.all(),
        required=False,
        label='Year levels',
        widget=forms.CheckboxSelectMultiple(),
    )
    curriculum_area = forms.ModelMultipleChoiceField(
        queryset=CurriculumLearningArea.objects.all(),
        required=False,
        label='Curriculum learning areas',
        widget=forms.CheckboxSelectMultiple(),
    )

    def search(self):
        """Search index based off query.

        This method overrides the default ModelSearchForm search method to
        modify the default result if a blank query string is given. The form
        returns all items instead of zero items if a blank string is given.

        The original search method checks if the form is valid, however
        with all fields being optional with no validation, the form is always
        valid. Therefore logic for an invalid form is removed.

        Returns:
            SearchQuerySet of search results of resources.
        """
        if not self.cleaned_data.get('q'):
            search_query_set = all_items(self.searchqueryset)
        else:
            search_query_set = self.searchqueryset.auto_query(self.cleaned_data['q'])

        # Only search models
        search_query_set = search_query_set.models(Resource)

        # Filter items by tags if given in query.
        # Currently the given filter is provided as a QuerySet, but the search
        # index saves the tags of objects as a list of primary
        # keys, stored as strings. Because of this, the logic below must
        # covert the QuerySet of the filter into a list of primary key strings.
        if self.cleaned_data['lang']:
            primary_keys = list(map(str, self.cleaned_data['lang'].values_list('pk', flat=True)))
            search_query_set = search_query_set.filter(
                languages__in=primary_keys
            )
        if self.cleaned_data['tech_area']:
            primary_keys = list(map(str, self.cleaned_data['tech_area'].values_list('pk', flat=True)))
            search_query_set = search_query_set.filter(
                technological_areas__in=primary_keys
            )
        if self.cleaned_data['progress_outcome']:
            primary_keys = list(map(str, self.cleaned_data['progress_outcome'].values_list('pk', flat=True)))
            search_query_set = search_query_set.filter(
                progress_outcomes__in=primary_keys
            )
        if self.cleaned_data['nzqa_standard']:
            primary_keys = list(map(str, self.cleaned_data['nzqa_standard'].values_list('pk', flat=True)))
            search_query_set = search_query_set.filter(
                nzqa_standards__in=primary_keys
            )
        if self.cleaned_data['year_level']:
            primary_keys = list(map(str, self.cleaned_data['year_level'].values_list('pk', flat=True)))
            search_query_set = search_query_set.filter(
                year_levels__in=primary_keys
            )
        if self.cleaned_data['curriculum_area']:
            primary_keys = list(map(str, self.cleaned_data['curriculum_area'].values_list('pk', flat=True)))
            search_query_set = search_query_set.filter(
                curriculum_learning_areas__in=primary_keys
            )
        return search_query_set


def all_items(searchqueryset):
    """Return all items of SearchQuerySet.

    Args:
        searchqueryset (SearchQuerySet): QuerySet of search items.

    Returns:
        All items in index.
    """
    return searchqueryset.all()
