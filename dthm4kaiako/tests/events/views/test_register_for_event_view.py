from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from users.models import User
from events.models import (
    Event,
    ParticipantType,
    EventRegistration
)
import datetime
import pytz
from events.views import register_for_event_view
from unittest import mock
from django.test.client import RequestFactory

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class RegisterForEventViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()
        EventRegistration.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_returns_200_when_event_exists_and_logged_in(self):
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
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:register', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_returns_302_when_event_exists_and_not_logged_in(self):
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
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:register', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], f'/accounts/login/?next=/events/register/{event.pk}/')

    # TODO: fix mocking issue
    # @mock.patch('events.views.ParticipantTypeForm')
    # @mock.patch('events.views.EventRegistrationForm')
    # @mock.patch('events.views.UserUpdateDetailsForm')
    # @mock.patch('events.views.BillingDetailsForm')
    # @mock.patch('events.views.TermsAndConditionsForm')
    # @mock.patch('events.views.emergency_details_valid')
    # @mock.patch('events.views.validate_event_registration_form')
    # @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    # def test_register_successfully_for_event(
    #     self,
    #     mocked_participant_type_form,
    #     mocked_registration_form,
    #     mocked_user_update_details_form,
    #     mocked_billing_details_form,
    #     mocked_terms_and_conditions_form,
    #     mocked_emergency_details_valid,
    #     mocked_validate_event_registration_form
    # ):
    #     event = Event.objects.create(
    #         name="Security in CS",
    #         description="description",
    #         registration_type=2,
    #         start=datetime.datetime(2023, 2, 13),
    #         end=datetime.datetime(2023, 2, 14),
    #         accessible_online=False,
    #         published=True
    #     )
    #     event.save()
    #     user = User.objects.create_user(
    #         id=1,
    #         username='kate',
    #         first_name='Kate',
    #         last_name='Bush',
    #         email='kate@uclive.ac.nz',
    #         password='potato',
    #     )
    #     user.save()
    #     self.client.force_login(user)

    #     participant_type = ParticipantType.objects.create(name="Teacher", price="10.00")
    #     event.participant_types.set([participant_type])
    #     event.save()
    #     kwargs = {
    #         'pk': event.pk,
    #         }
    #     url = reverse('events:register', kwargs=kwargs)
    #     self.factory = RequestFactory()
    #     request = self.factory.post(url)
    #     request.user = user

    #     mocked_participant_type_form.is_valid = True
    #     mocked_participant_type_form.return_value.cleaned_data = {
    #         "participant_type": 2,
    #     }
    #     mocked_registration_form.is_valid = True
    #     mocked_registration_form.return_value.cleaned_data = {
    #         'emergency_contact_first_name': "Bob",
    #         'emergency_contact_last_name': "Ross",
    #         'emergency_contact_phone_number': "123456789",
    #         'emergency_contact_relationship': "Jeff",
    #     }
    #     mocked_user_update_details_form.is_valid = True
    #     mocked_user_update_details_form.return_value.cleaned_data = {
    #         'first_name': "Franz",
    #         'last_name': "Joseph",
    #         'educational_entities': '1',
    #         'user_region': '1',
    #         'email_address': "test@test.com",
    #         'mobile_phone_number': '123456789'
    #     }
    #     mocked_billing_details_form.is_valid = True
    #     mocked_billing_details_form.return_value.cleaned_data = {
    #     }
    #     mocked_terms_and_conditions_form.is_valid = True
    #     mocked_terms_and_conditions_form.return_value.cleaned_data = {
    #     }

    #     register_for_event_view(request, event.pk)
    #     self.assertEqual(EventRegistration.objects.all().count(), 1)

    #     self.assertEqual(EventRegistration.objects.filter(event=event, user=user).count(), 1)
