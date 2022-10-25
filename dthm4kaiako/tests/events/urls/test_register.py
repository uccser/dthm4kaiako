"""Unit tests for register url"""

from django.urls import reverse, resolve
from events.models import Event
from tests.BaseTestWithDB import BaseTestWithDB
import datetime


class RegisterURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_register_url(self):
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
        url = reverse('events:register', kwargs=kwargs)
        expected_url = f"/events/register/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_register_resolve_provides_correct_view_name(self):
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
        pk = event.pk
        self.assertEqual(resolve(f"/events/register/{pk}/").view_name, "events:register")
