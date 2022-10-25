"""Unit tests for session model"""

from events.models import Session, Event
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
import datetime

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class SessionTests(BaseTestWithDB):

    # ------------------------------- tests for __str__ ----------------------------
    def test_str_representation(self):

        event = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event.save()
        session = Session.objects.create(
            id=1,
            name="session 2",
            description="some description",
            start=datetime.datetime(2023, 6, 24, 13, 0, 0),
            end=datetime.datetime(2023, 6, 24, 16, 0, 0),
            event=Event.objects.get(id=1),
        )
        session.save()
        self.assertEqual(
            str(session),
            session.name
        )
