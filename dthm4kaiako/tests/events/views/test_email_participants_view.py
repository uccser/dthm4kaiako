"""Unit tests for email_participants_view"""

from django.urls import reverse
from events.models import (
    Event,
    ParticipantType,
    Address,
    EventRegistration
)
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime
from django.test.utils import override_settings
from http import HTTPStatus


class EmailParticipantsURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        EventRegistration.objects.all().delete()
        Event.objects.all().delete()
        ParticipantType.objects.all().delete()
        Address.objects.all().delete()
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_email_participants_view_returns_200_when_event_exists(self):
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
            'event_pk': event.pk,
            }
        url = reverse('events:email_participants', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    # TODO: not sure how to test emails are sent
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_email_participants_view_and_logged_in_and_staff_then_successfully_emailed(self):
        pass

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_email_participants_view_and_not_logged_in_and_staff_then_stay_on_same_page(self):
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
            'event_pk': event.pk,
            }
        url = reverse('events:email_participants', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_email_participants_view_and_logged_in_and_not_staff_then_redirected(self):
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
            'event_pk': event.pk,
            }
        url = reverse('events:email_participants', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertEqual(response['Location'], '/events/manage/')
