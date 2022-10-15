"""Unit tests for cancel event url"""

from django.urls import reverse, resolve
from events.models import Event
from tests.BaseTestWithDB import BaseTestWithDB
import datetime


class CancelEventURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_cancel_event_url(self):
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
        updated_event = Event.objects.filter(pk=1)
        updated_event.update(published=True)
        event.save()
        url = reverse('events:cancel_event', kwargs=kwargs)
        expected_url = f"/events/manage/cancel_event/{event.pk}/"
        self.assertEqual(url, expected_url)

    def test_cancel_event_resolve_provides_correct_view_name(self):
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
        self.assertEqual(resolve(f"/events/manage/cancel_event/{event.pk}/").view_name, "events:cancel_event")
