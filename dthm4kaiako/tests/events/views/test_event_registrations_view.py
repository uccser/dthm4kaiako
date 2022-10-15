from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from users.models import User
from events.models import (
    Event,
    Location
)
import datetime
import pytz
from django.contrib.gis.geos import Point
import datetime
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')

class EventRegistrationsViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        Location.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_registrations_gives_200_status_code(self):

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
        url = reverse("events:event_registrations")
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
