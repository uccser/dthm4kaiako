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
    RegistrationForm
)
# from events.views import manage_event_details_view
# from unittest import mock
# from django.test.client import RequestFactory
# from django.contrib import messages

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class ManageEventDetailsURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        Location.objects.all().delete()
        RegistrationForm.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_registration_form_details_view_returns_200_when_event_exists(self):
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
        url = reverse('events:manage_event_registration_form_details', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    # TODO: fix mocking issue
    # @mock.patch('events.views.ManageEventRegistrationFormDetailsForm')
    # @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    # def test_manage_event_registration_form_details_view_and_logged_in_and_staff_then_successfully_update(
    #     self,
    #     mock_form_class
    # ):
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
    #         start=datetime.datetime(2023, 6, 24, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
    #         end=datetime.datetime(2023, 6, 26, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
    #         accessible_online=False,
    #         published=True
    #     )
    #     event_physical_register_1.locations.set([location_1])
    #     event_physical_register_1.save()

    #     event = Event.objects.get(pk=event_physical_register_1.pk)
    #     event.event_staff.set([user_kate])
    #     event.save()
    #     self.client.force_login(user_kate)
    #     kwargs = {
    #         'pk': event.pk,
    #         }
    #     self.factory = RequestFactory()
    #     updated_terms_and_conditions = "New Ts and Cs here"
    #     url = reverse('events:manage_event_registration_form_details', kwargs=kwargs)
    #     request = self.factory.post(url, {"terms_and_conditions": updated_terms_and_conditions})
    #     request.user = user_kate
    #     # Add support  django messaging framework
    #     request._messages = messages.storage.default_storage(request)

    #     mock_form_class.is_valid = True
    #     mock_form_class.return_value.cleaned_data = {
    #         "terms_and_conditions": updated_terms_and_conditions
    #     }
    #     response = manage_event_details_view(request, event.pk)
    #     updated_event = RegistrationForm.objects.get(event=event.pk)
    #     self.assertEqual(updated_event.terms_and_conditions, updated_terms_and_conditions)
    #     self.assertEqual(HTTPStatus.OK, response.status_code)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_registration_form_details_view_and_not_logged_in_and_staff_then_redirected(self):
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
        event.event_staff.set([user_kate])
        event.save()
        url = reverse('events:manage_event_registration_form_details', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(
            response['Location'],
            f'/accounts/login/?next=/events/manage-event-registration-form-details/{event.pk}/'
        )

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_registration_form_details_view_and_logged_in_and_not_staff_then_redirected(self):
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
        self.client.force_login(user_kate)

        event = Event.objects.get(pk=event_physical_register_1.pk)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:manage_event_registration_form_details', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/manage/')
