"""Utilithy functions for POET application."""

import random
from poet.models import Resource


def select_resources_for_poet_form(request):
    """Select resources for POET form based off user request.

    Args:
        request (Request): Request object.

    Returns:
        List of resource objects.
    """
    random.sample(list(Resource.objects.all()), 3)
    resources = random.sample(list(Resource.objects.all()), 3)
    return resources
