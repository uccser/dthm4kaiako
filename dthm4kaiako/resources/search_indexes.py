from haystack import indexes
from resources.models import (
    Resource,
    Language,
)


class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    languages = indexes.FacetMultiValueField()

    def prepare_languages(self, obj):
        """Create data for languages index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of language primary keys as strings.
        """
        primary_keys = list(obj.languages.all().values_list("pk", flat=True))
        return primary_keys


    def get_model(self):
        return Resource
