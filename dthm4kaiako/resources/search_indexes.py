"""Index for resource application."""

from django.template.loader import render_to_string
from resources.models import Resource, Language


class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    """Index for resource objects."""

    text = indexes.CharField(document=True, use_template=True)
    languages = indexes.MultiValueField()
    technological_areas = indexes.MultiValueField()
    progress_outcomes = indexes.MultiValueField()
    nzqa_standards = indexes.MultiValueField()
    year_levels = indexes.MultiValueField()
    curriculum_learning_areas = indexes.MultiValueField()
    html_result = indexes.CharField(indexed=False)

    def prepare_languages(self, obj):
        """Create data for languages index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of primary keys as strings.
        """
        return list(obj.languages.all().values_list("pk", flat=True))

    def prepare_technological_areas(self, obj):
        """Create data for technological areas index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of primary keys as strings.
        """
        return list(obj.technological_areas.all().values_list("pk", flat=True))

    def prepare_progress_outcomes(self, obj):
        """Create data for progress outcomes index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of primary keys as strings.
        """
        return list(obj.progress_outcomes.all().values_list("pk", flat=True))

    def prepare_nzqa_standards(self, obj):
        """Create data for NZQA standards index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of primary keys as strings.
        """
        return list(obj.nzqa_standards.all().values_list("pk", flat=True))

    def prepare_year_levels(self, obj):
        """Create data for year levels index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of primary keys as strings.
        """
        return list(obj.year_levels.all().values_list("pk", flat=True))

    def prepare_curriculum_learning_areas(self, obj):
        """Create data for year levels index value.

        Args:
            obj (Resource): Resource object.

        Returns:
            List of primary keys as strings.
        """
        return list(obj.curriculum_learning_areas.all().values_list("pk", flat=True))

    def prepare_html_result(self, obj):
        """Create HTML for result.

        Args:
            obj (Resource): Resource object.

        Returns:
            String of HTML for rendering as result.
        """
        context = {
            'resource': obj,
            'languages': Language.objects.all(),
        }
        return render_to_string('resources/resource-card.html', context=context)

    def get_model(self):
        """Return model for search index.

        Returns:
            Resource class.
        """
        return Resource

    def index_queryset(self, using=None):
        """Return queryset of items to index."""
        return Resource.objects.filter(published=True)
