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
from events.views import generate_event_registrations_csv_view
from unittest import mock
from django.contrib import messages
from django.test.utils import override_settings


class GenerateEventRegistrationsCSVViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Location.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: fix mocking issue
    # @mock.patch('events.views.ManageEventDetailsForm')
    # @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    # def test_generate_event_registrations_csv_views_returns_200_when_event_exists(self, mock_form_class):
    #     user_kate = User.objects.create_user(
    #         id=1,
    #         username='kate',
    #         first_name='Kate',
    #         last_name='Bush',
    #         email='kate@uclive.ac.nz',
    #         password='potato',
    #     )
    #     user_kate.save()

    #     location_1 = Location.objects.create(
    #         id=1,
    #         room='Room 123',
    #         name='Middleton Grange School',
    #         street_address='12 High Street',
    #         suburb='Riccarton',
    #         city='Chrirstchurch',
    #         region=14,
    #         coords=Point(-43, 172)
    #     )
    #     location_1.save()

    #     event_physical_register_1 = Event.objects.create(
    #         id=1,
    #         name="DTHM for Kaiako Conference 2023",
    #         description="description",
    #         registration_type=1,
    #         start=datetime.date(2023, 6, 24),
    #         end=datetime.date(2023, 6, 26),
    #         accessible_online=False,
    #         published=True
    #     )
    #     event_physical_register_1.locations.set([location_1])
    #     event_physical_register_1.save()

    #     event = Event.objects.get(pk=event_physical_register_1.pk)
    #     event.event_staff.set([user_kate])
    #     event.save()
    #     self.client.force_login(user_kate)

    #     self.factory = RequestFactory()
    #     url = reverse('events:generate_event_csv')
    #     request = self.factory.post(url)
    #     request.user = user_kate
    #     # Add support  django messaging framework
    #     request._messages = messages.storage.default_storage(request)

    #     mock_form_class.is_valid = True
    #     mock_form_class.return_value.cleaned_data = {
    #         'file_name': "Some random name",
    #         'event_name': True,
    #         'submitted_datetime': True,
    #         'updated_datetime': True,
    #         'status': True,
    #         'participant_type': True,
    #         'staff_comments': True,
    #         'participant_first_name': True,
    #         'participant_last_name': True,
    #         'dietary_requirements': True,
    #         'educational_entities': True,
    #         'region': True,
    #         'mobile_phone_number': True,
    #         'email_address': True,
    #         'how_we_can_best_accommodate_them': True,
    #         'emergency_contact_first_name': True,
    #         'emergency_contact_last_name': True,
    #         'emergency_contact_relationship': True,
    #         'emergency_contact_phone_number': True,
    #         'paid': True,
    #         'billing_email_address': True,
    #         'admin_billing_comments': True,
    #         'representing': True,
    #         'bill_to': True,
    #         'billing_physical_address': True

    #     }
    #     response = generate_event_registrations_csv_view(request, event.pk)
    #     self.assertEqual(HTTPStatus.OK, response.status_code)
