"""Unit tests for manage_event_details url"""

import pytz
from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event
from users.models import User
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_event_registrations,
    generate_serieses,
)
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from django.test.utils import override_settings
from users.models import User
from django.contrib.gis.geos import Point
import datetime
from events.models import (
    Location,
    Event,
)
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class ManageEventDetailsURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        Location.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_manage_event_details_url(self):
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2023, 6, 26, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:manage_event_details', kwargs=kwargs)
        expected_url = f"/events/manage-event-details/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_manage_event_details_resolve_provides_correct_view_name(self):
        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2023, 6, 26, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertEqual(
            resolve(f"/events/manage-event-details/{event.pk}/").view_name,
            "events:manage_event_details"
        )
