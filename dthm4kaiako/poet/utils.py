"""Utilithy functions for POET application."""

import random
from poet.models import Resource
from poet.settings import NUM_RESOURCES_PER_FORM


def select_resources_for_poet_form(progress_outcome_group):
    """Select resources for POET form based off user request.

    Args:
        progress_outcome_group (ProgressOutcomeGroup): Group selected by user in form.

    Returns:
        List of resource pks.
    """
    all_resources = Resource.objects.filter(
        active=True,
        target_progress_outcome__in=progress_outcome_group.progress_outcomes.all(),
    ).values_list('pk', flat=True)
    return random.sample(list(all_resources), NUM_RESOURCES_PER_FORM)
