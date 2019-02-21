"""Module for forms for resource module."""


from django import forms
from haystack.forms import FacetedSearchForm
from resources.models import (
    Resource,
    Language,
)


class ResourceSearchForm(FacetedSearchForm):
    """Class for resource search form."""

    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=False,
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
        if self.cleaned_data['languages']:
            primary_keys = list(map(str, self.cleaned_data['languages'].values_list('pk', flat=True)))
            search_query_set = search_query_set.filter(
                languages__in=primary_keys
            )

        return search_query_set

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).
        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset.all()


def all_items(searchqueryset):
    """Return all items of SearchQuerySet.

    Args:
        searchqueryset (SearchQuerySet): QuerySet of search items.

    Returns:
        All items in index.
    """
    return searchqueryset.all()
