"""Unit tests for event url"""

from django.urls import reverse, resolve
from http import HTTPStatus
from django.test.utils import override_settings
from events.models import Event
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime


class EventURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        User.objects.all().delete()
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_valid_event_details_url(self):
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
            'slug': event.slug
            }
        url = reverse('events:event', kwargs=kwargs)
        expected_url = f"/events/event/{event.pk}/{event.slug}/"
        self.assertEqual(url, expected_url)

    def test_event_details_resolve_provides_correct_view_name(self):
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
        pk = event.pk
        slug = event.slug
        self.assertEqual(resolve(f"/events/event/{pk}/{slug}/").view_name, "events:event")

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_event_details_url_returns_200_when_event_exists(self):
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
            'slug': event.slug
            }
        url = reverse('events:event', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
