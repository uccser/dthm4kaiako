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
    resources = random.sample(list(Resource.objects.all()), 3)
    return resources

def check_poet_form_is_valid(request):
    is_valid = True
    # Get number of resources from session
    resource_pks = request.session.get('poet_form_resources', list())
    for i, resource_pk in enumerate(resource_pks):
        request.POST
    # Check number matches POST data
    # Check choice exists for each form
