"""Filters for the event application."""

import django_filters
from events.models import Event


class EventFilter(django_filters.FilterSet):
    """Filter for an event."""

    start = django_filters.DateTimeFilter()

    class Meta:
        """Metadata for filter."""
        model = Event
        fields = (
            'accessible_online',
            'locations__region',
            'start',
            'end',
        )
