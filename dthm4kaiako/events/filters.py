"""Filters for events application."""

import django_filters
from django.utils.timezone import now
from events.models import (
    Event,
    Location,
    Organiser,
)


class UpcomingEventFilter(django_filters.FilterSet):
    """Filter for showing upcoming events."""

    locations__region = django_filters.ChoiceFilter(
        choices=Location.REGION_CHOICES,
        label='Region',
        empty_label='Show all',
    )
    accessible_online = django_filters.ChoiceFilter(
        choices=(
            ('1', 'Yes'),
            ('0', 'No'),
        ),
        empty_label='Show all',
    )
    organisers = django_filters.ModelChoiceFilter(
        queryset=Organiser.objects.all(),
        label='Organiser',
        empty_label='Show all',
    )

    class Meta:
        """Meta options."""

        model = Event
        fields = [
            'locations__region',
            'accessible_online',
        ]

    @property
    def qs(self):
        """Return filtered queryset of upcoming events."""
        return super().qs.filter(
            published=True
        ).filter(
            end__gte=now()
        ).order_by('start').prefetch_related(
            'organisers',
            'locations',
            'sponsors',
        ).select_related(
            'series',
        ).distinct()


class PastEventFilter(django_filters.FilterSet):
    """Filter for showing past events."""

    locations__region = django_filters.ChoiceFilter(
        choices=Location.REGION_CHOICES,
        label='Region',
        empty_label='Show all',
    )
    accessible_online = django_filters.ChoiceFilter(
        choices=(
            ('1', 'Yes'),
            ('0', 'No'),
        ),
        empty_label='Show all',
    )
    organisers = django_filters.ModelChoiceFilter(
        queryset=Organiser.objects.all(),
        label='Organiser',
        empty_label='Show all',
    )

    class Meta:
        """Meta options."""

        model = Event
        fields = [
            'locations__region',
            'accessible_online',
        ]

    @property
    def qs(self):
        """Return filtered queryset of past events."""
        return super().qs.filter(
            published=True
        ).filter(
            end__lt=now()
        ).order_by('-end').prefetch_related(
            'organisers',
            'locations',
            'sponsors',
        ).select_related(
            'series',
        ).distinct()
