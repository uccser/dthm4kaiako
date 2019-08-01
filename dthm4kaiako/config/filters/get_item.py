"""Template filter for getting a value from a dictionary."""

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    """Return value from dictionary.

    Args:
        dictionary (dict): Dictionary to retrieve value from.
        key (str): Key to perform lookup.

    Returns:
        Value of key in dictionary.
    """
    return dictionary.get(key)
