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

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_details_url_returns_200_when_event_exists(self):
        user_kate = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

        location_1 = Location.objects.create(
            id=1,
            room='Room 123',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-43, 172)
        )
        location_1.save()

        event_physical_register_1 = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2023, 6, 26, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event_physical_register_1.locations.set([location_1])
        event_physical_register_1.save()
        
        event = Event.objects.get(pk=event_physical_register_1.pk)
        event.event_staff.set([user_kate])
        event.save()
        self.client.force_login(user_kate)

        kwargs = {
            'pk': event.pk,
            }

        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        url = reverse('events:manage_event_details', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
