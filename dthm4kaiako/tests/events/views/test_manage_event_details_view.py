"""Unit tests for manage_event_details_views"""

import pytz
from django.urls import reverse
from http import HTTPStatus
from users.models import User
from tests.BaseTestWithDB import BaseTestWithDB
from django.test.utils import override_settings
from django.contrib.gis.geos import Point
import datetime
from events.models import (
    Location,
    Event,
)
from events.views import manage_event_details_view
from unittest import mock
from django.test.client import RequestFactory
from django.contrib import messages

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class ManageEventDetailsURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        Location.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @mock.patch('events.views.ManageEventDetailsForm')
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_details_view_returns_200_when_event_exists(self, mock_form_class):
        user_kate = User.objects.create_user(
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
        expected_description = "new description here"
        self.factory = RequestFactory()
        url = reverse('events:manage_event_details', kwargs=kwargs)
        request = self.factory.post(url)
        # Add support  django messaging framework
        request._messages = messages.storage.default_storage(request)
        request.user = user_kate

        mock_form_class.is_valid = True
        mock_form_class.return_value.cleaned_data = {
            "name": event.name,
            "description": expected_description,
            "show_schedule": event.show_schedule,
            "featured": event.featured,
            "registration_type": event.registration_type,
            "external_event_registration_link": event.external_event_registration_link,
            "start": event.start,
            "end": event.end,
            "accessible_online": event.accessible_online,
            "is_catered": event.is_catered,
            "contact_email_address": event.contact_email_address,
            "series": event.series,
            "capacity": event.capacity,
            "locations": event.locations.all(),
            "sponsors": event.sponsors.all(),
            "organisers": event.organisers.all(),
            "event_staff": event.event_staff.all(),
        }
        response = manage_event_details_view(request, event.pk)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)  # redirect to mange event page
        self.assertEqual(response['Location'], f'/events/manage/{event.pk}/')

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_details_view_and_not_logged_in_and_staff_member_then_redirect(self):
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
        kwargs = {
            'pk': event.pk,
            }
        user = User.objects.get(pk=1)
        event.event_staff.set([user])
        event.save()
        url = reverse('events:manage_event_details', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], f'/accounts/login/?next=/events/manage-event-details/{event.pk}/')

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_details_view_and_logged_in_and_not_staff_member_then_redirect(self):
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
        self.client.force_login(user_kate)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:manage_event_details', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/manage/')
