from django.template.loader import render_to_string
from haystack import indexes
from resources.models import (
    Resource,
    Language,
)


class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    languages = indexes.FacetMultiValueField()
    html_result = indexes.CharField(indexed=False)

    def prepare_languages(self, obj):
        """Create data for languages index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of language primary keys as strings.
        """
        primary_keys = list(obj.languages.all().values_list("pk", flat=True))
        return primary_keys

    def prepare_html_result(self, obj):
        """Create HTML for result.

        Args:
            obj (Resource): Resource object.

        Returns:
            String of HTML for rendering as result.
        """
        return render_to_string('resources/resource-card.html', context={'resource': obj})


    def get_model(self):
        return Resource
