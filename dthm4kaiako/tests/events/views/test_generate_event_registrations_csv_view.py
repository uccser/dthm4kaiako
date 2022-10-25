"""Unit tests for generate_event_registrations_csv_view """

from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from events.models import (
    Location,
    Event,
)


class GenerateEventRegistrationsCSVViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Location.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
