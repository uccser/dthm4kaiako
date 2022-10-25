"""Unit tests for generate_event_csv_view """

from django.urls import reverse
from http import HTTPStatus
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from django.contrib.gis.geos import Point
import datetime
from events.models import (
    Location,
    Event,
)
from django.test import RequestFactory
from events.views import generate_event_csv_view
from unittest import mock


class GenerateEventCSVViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Location.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @mock.patch('events.views.BuilderFormForEventsCSV')
    def test_generate_event_csv_url_returns_200_when_event_exists(self, mock_form_class):
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

        self.factory = RequestFactory()
        url = reverse('events:generate_event_csv')
        request = self.factory.post(url)
        request.user = user_kate
        request.event = event

        mock_form_class.is_valid = True
        mock_form_class.return_value.cleaned_data = {
            'file_name': "Some random name",
            'event_name': True,
            'description': True,
            'published_status': True,
            'show_schedule': True,
            'featured_status': True,
            'registration_type': True,
            'external_event_registration_link': True,
            'start_datetime': True,
            'end_datetime': True,
            'accessible_online': True,
            'is_free': True,
            'locations': True,
            'sponsors': True,
            'organisers': True,
            'series': True,
            'is_catered': True,
            'contact_email_address': True,
            'event_staff': True,
            'is_cancelled': True,
            'approved_registrations_count': True,
            'pending_registrations_count': True,
            'declined_registrations_count': True,
            'withdrawn_registrations_count': True,
        }

        response = generate_event_csv_view(request)
        self.assertEqual(HTTPStatus.OK, response.status_code)
