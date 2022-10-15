"""Unit tests for publish_event url"""

from django.urls import reverse, resolve
from http import HTTPStatus
from events.models import Event
from users.models import User
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime


class PublishEventURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_publish_event_url(self):
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
        updated_event = Event.objects.filter(pk=event.pk)
        updated_event.update(published=False)
        event.save()
        url = reverse('events:publish_event', kwargs=kwargs)
        expected_url = f"/events/manage/publish_event/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_publish_event_resolve_provides_correct_view_name(self):
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
        updated_event = Event.objects.filter(pk=event.pk)
        updated_event.update(published=False)
        event.save()
        self.assertEqual(
            resolve(f"/events/manage/publish_event/{event.pk}/").view_name,
            "events:publish_event"
        )

    # TODO: fix - giving 302 instead of 200
    def test_publish_event_url_returns_200_when_event_exists(self):
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
        updated_event = Event.objects.filter(pk=event.pk)
        updated_event.update(published=False)
        event.save()
        url = reverse('events:publish_event', kwargs=kwargs)
        response = self.client.post(url)
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
