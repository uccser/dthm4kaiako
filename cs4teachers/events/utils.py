"""Utility functions for the events application."""

from datetime import datetime
from django.db.models import DateField
from django.db.models.aggregates import Max, Min
from events.models import (
    Event,
    ThirdPartyEvent,
)


class GenericEvent:
    """Object combining common attributes of Event and ThirdPartyEvent classes."""

    def __init__(self, name, absolute_url, start_date, end_date, third_party=False):
        """Construct GenericEvent object.

        Args:
            name: The name of the vent (str).
            absolute_url: The URL of the event page (str).
            start_date: Date the event starts (date).
            end_date: Date the event ends (date).
            third_party: True if event is a third party event, otherwise False.
        """
        self.name = name
        self.absolute_url = absolute_url
        self.start_date = start_date
        self.end_date = end_date
        self.third_party = third_party


def retrieve_all_events(upcoming=False):
    """Retrieve both events and third party events.

    These are returned in sorted order by start datetime,
    then end datetime.

    Args:
        upcoming (bool): If True, only return events after the current datetime.
            Default is False.

    Returns:
        List of event objects (list).
    """
    all_events = []
    today = datetime.today()

    events = Event.objects.filter(
        is_published=True
    ).annotate(
        start_date=Min("sessions__start_datetime", output_field=DateField()),
        end_date=Max("sessions__end_datetime", output_field=DateField()),
    )

    third_party_events = ThirdPartyEvent.objects.filter(
        is_published=True
    )

    if upcoming:
        events = events.filter(end_date__gte=today)
        third_party_events = third_party_events.filter(end_date__gte=today)

    for event in events:
        all_events.append(GenericEvent(
            event.name,
            event.get_absolute_url(),
            event.start_date.date(),
            event.end_date.date(),
        ))

    for event in third_party_events:
        all_events.append(GenericEvent(
            event.name,
            event.get_absolute_url(),
            event.start_date,
            event.end_date,
            True,
        ))

    return sorted(all_events, key=lambda x: (x.start_date, x.end_date))
