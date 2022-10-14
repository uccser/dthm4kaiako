from django.urls import reverse, resolve
from http import HTTPStatus
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from users.models import User
from django.contrib.gis.geos import Point
import datetime
from events.models import (
    Location,
    Event,
)


class GenerateEventCSVURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_generate_event_csv_url(self):
        url = reverse('events:generate_event_csv')
        expected_url = "/events/manage/generate_event_csv/"
        self.assertEqual(url, expected_url)

    def test_generate_event_csv_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/manage/generate_event_csv/").view_name, "events:generate_event_csv")

    def test_generate_event_csv_url_returns_200_when_event_exists(self):
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

        # TODO: need to mock the request

        url = reverse('events:generate_event_csv')
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
