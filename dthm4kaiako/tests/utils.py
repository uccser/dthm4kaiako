"""Utility functions for testing."""

import random
from events.models import EventApplication


def random_boolean(percent=50):
    """Return a random boolean.

    Args:
        Percentage (int): Chance the value is True.

    Returns:
        Random boolean value.
    """
    return random.randrange(100) < percent



def random_event_application_status():
    """Return a random status from the availbale choices on the EventApplication model."""
    status_choices = [c[0] for c in EventApplication.STATUS_CHOICES]
    return random.choice(status_choices)
