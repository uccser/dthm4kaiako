"""Unit tests for is_in_past_or_cancelled"""

from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
import datetime
import pytz
from events.models import (
    Event,
)
from events.views import is_in_past_or_cancelled
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class IsInPastOrCancelledTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_is_in_past_or_cancelled_and_in_past_and_not_cancelled(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2021, 2, 13, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2021, 2, 14, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True
        )
        event.save()
        self.assertTrue(is_in_past_or_cancelled(event))

    def test_is_in_past_or_cancelled_and_in_past_and_cancelled(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2021, 2, 13, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2021, 2, 14, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True,
            is_cancelled=True,
        )
        event.save()
        self.assertTrue(is_in_past_or_cancelled(event))

    def test_is_in_past_or_cancelled_and_in_future_and_cancelled(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2090, 2, 13, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2090, 2, 14, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True,
            is_cancelled=True,
        )
        event.save()
        self.assertTrue(is_in_past_or_cancelled(event))

    def test_is_in_past_or_cancelled_and_in_future_and_not_cancelled(self):
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2090, 2, 13, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            end=datetime.datetime(2090, 2, 14, 0, 0, 0, 00, NEW_ZEALAND_TIME_ZONE),
            accessible_online=False,
            published=True,
            is_cancelled=False,
        )
        event.save()
        self.assertFalse(is_in_past_or_cancelled(event))
