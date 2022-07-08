"""Search utility functions."""

from django.db.models import Value
from django.contrib.postgres.search import SearchVector


def concat_field_values(*args):
    """Return string of field values for search indexing.

    Args:
        Any number of QuerySet objects, the result of value_list calls.

    Returns:
        String for search indexing.
    """
    field_names = []
    for queryset in args:
        for instance in queryset:
            for field in instance:
                field_names.append(str(field))
    return ' '.join(field_names)


def get_search_index_updater(instance):
    """Return function for updating search index of instance."""
    components = instance.index_contents()
    pk = instance.pk

    def on_commit():
        search_vector_list = []
        for weight, text in components.items():
            search_vector_list.append(
                SearchVector(Value(text), weight=weight)
            )
        search_vectors = search_vector_list[0]
        for search_vector in search_vector_list[1:]:
            search_vectors += search_vector

        instance.__class__.objects.filter(pk=pk).update(
            search_vector=search_vectors
        )
        print(f'Rebuilt index for {instance}')
    return on_commit
