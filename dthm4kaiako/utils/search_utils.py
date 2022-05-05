"""Search utility functions."""


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
