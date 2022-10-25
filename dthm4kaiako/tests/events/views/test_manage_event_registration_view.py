"""Unit tests for manage_event_registration_view"""

from django.urls import reverse
from http import HTTPStatus
from events.models import (
    Event,
    EventRegistration,
    ParticipantType,
    Address,
)
from tests.BaseTestWithDB import BaseTestWithDB
from django.test.utils import override_settings
import datetime
from events.views import manage_event_registration_view
from unittest import mock
from django.test.client import RequestFactory
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


class ManageEventRegistrationViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        EventRegistration.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @mock.patch('events.views.ManageEventRegistrationFormDetailsForm')
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_registration_view_returns_200_when_event_exists(self, mock_form_class):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        user = User.objects.create_user(
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        self.client.force_login(user)

        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")

        billing_address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address.save()

        event_registration = EventRegistration.objects.create(
            participant_type=participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()
        kwargs = {
            'pk_event': event.pk,
            'pk_registration': event_registration.pk
            }
        event.event_staff.set([user])
        event.save()
        url = reverse('events:manage_event_registration', kwargs=kwargs)

        self.factory = RequestFactory()
        request = self.factory.post(url)
        request.user = user
        # Add support  django messaging framework
        request._messages = messages.storage.default_storage(request)
        updated_staff_comments = "staff comments"

        mock_form_class.is_valid = True
        mock_form_class.return_value.cleaned_data = {
            "terms_and_conditions": updated_staff_comments
        }
        response = manage_event_registration_view(request, event.pk, event_registration.pk)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @mock.patch('events.views.ManageEventRegistrationFormDetailsForm')
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_registration_view_and_not_logged_in_and_staff_then_redirect(self, mock_form_class):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        user = User.objects.create_user(
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()

        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")

        billing_address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address.save()

        event_registration = EventRegistration.objects.create(
            participant_type=participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()
        kwargs = {
            'pk_event': event.pk,
            'pk_registration': event_registration.pk
            }
        event.event_staff.set([user])
        event.save()

        url = reverse('events:manage_event_registration', kwargs=kwargs)

        self.factory = RequestFactory()
        request = self.factory.post(url)
        request.user = user
        # Add support  django messaging framework
        request._messages = messages.storage.default_storage(request)
        updated_staff_comments = "staff comments"

        mock_form_class.is_valid = True
        mock_form_class.return_value.cleaned_data = {
            "terms_and_conditions": updated_staff_comments
        }
        response = manage_event_registration_view(request, event.pk, event_registration.pk)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @mock.patch('events.views.ManageEventRegistrationFormDetailsForm')
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_manage_event_registration_view_and_logged_in_and_not_staff_then_redirect(self, mock_form_class):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.save()
        user = User.objects.create_user(
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        self.client.force_login(user)

        participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")

        billing_address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address.save()

        event_registration = EventRegistration.objects.create(
            participant_type=participant_type,
            user=user,
            event=event,
            billing_physical_address=billing_address,
            billing_email_address="test@test.co.nz"
        )
        event_registration.status = 1
        event_registration.save()

        kwargs = {
            'pk_event': event.pk,
            'pk_registration': event_registration.pk
            }
        url = reverse('events:manage_event_registration', kwargs=kwargs)

        self.factory = RequestFactory()
        request = self.factory.post(url)
        # Add support  django messaging framework
        request._messages = messages.storage.default_storage(request)
        request.user = user
        updated_staff_comments = "staff comments"

        mock_form_class.is_valid = True
        mock_form_class.return_value.cleaned_data = {
            "terms_and_conditions": updated_staff_comments
        }
        response = manage_event_registration_view(request, event.pk, event_registration.pk)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/manage/')
