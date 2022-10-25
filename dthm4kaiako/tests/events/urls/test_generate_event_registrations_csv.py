"""Unit tests for generate_event_registrations_csv url"""

from django.urls import reverse, resolve
from events.models import (
    Event,
    Location,
)
from django.contrib.gis.geos import Point
import datetime
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User


class GenerateEventRegistrationsCSVURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Location.objects.all().delete()
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_generate_event_registrations_csv_url(self):
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
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
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
        url = reverse('events:generate_event_registrations_csv', kwargs=kwargs)
        expected_url = f"/events/manage/generate_event_registrations_csv/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_generate_event_registrations_csv_resolve_provides_correct_view_name(self):
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
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event_physical_register_1.locations.set([location_1])
        event_physical_register_1.save()

        event = Event.objects.get(pk=event_physical_register_1.pk)
        event.event_staff.set([user_kate])
        event.save()
        self.client.force_login(user_kate)
        self.assertEqual(resolve(
            f"/events/manage/generate_event_registrations_csv/{event.pk}/").view_name,
            "events:generate_event_registrations_csv"
            )
