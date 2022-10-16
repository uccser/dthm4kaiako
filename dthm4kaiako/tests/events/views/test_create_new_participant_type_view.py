"""Unit tests for create_new_participant_type_view"""

from django.urls import reverse
from http import HTTPStatus
from events.models import (
    Event,
    ParticipantType,
)
from users.models import User
from tests.BaseTestWithDB import BaseTestWithDB
import datetime
from unittest import mock


class CreateNewParticipantTypeViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_create_new_participant_type_view_returns_302_when_event_exists_and_logged_in(self):
        '''Redirect to manage event page.'''
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
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:create_new_participant_type', kwargs=kwargs)
        body = b'{"name": "Teacher", "price": "10.00"}'
        response = self.client.generic('POST', url, body)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], f'/events/manage/{event.pk}/')

    @mock.patch('events.views.ParticipantTypeCreationForm')
    def test_create_new_participant_type_view_and_logged_in_then_creates_new_participant_type_successfully(
        self,
        mock_form_class
    ):
        '''Redirect to manage event page.'''
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
        event.event_staff.set([user])
        event.save()
        self.client.force_login(user)
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:create_new_participant_type', kwargs=kwargs)

        mock_form_class.is_valid = True
        mock_form_class.return_value.cleaned_data = {
            'name': "Teacher",
            'price': "10.0"
        }
        self.client.post(url, {'name': "Teacher", 'price': "10.0"})
        self.assertEqual(ParticipantType.objects.last().name, "Teacher")

    def test_create_new_participant_type_view_returns_302_when_event_exists_and_not_logged_in(self):
        '''Redirect to login page.'''
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
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:create_new_participant_type', kwargs=kwargs)
        body = b'{"name": "Teacher", "price": "10.00"}'
        response = self.client.generic('POST', url, body)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(
            response['Location'],
            f'/accounts/login/?next=/events/manage/create_new_participant_type/{event.pk}/'
        )

    def test_create_new_participant_type_view_returns_302_when_event_exists_and_logged_in_and_not_staff(self):
        '''Redirect to all staff events page.'''
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
        kwargs = {
            'pk': event.pk,
            }
        url = reverse('events:create_new_participant_type', kwargs=kwargs)
        body = b'{"name": "Teacher", "price": "10.00"}'
        response = self.client.generic('POST', url, body)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/manage/')
