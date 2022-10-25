"""Unit tests for upcoming events url"""

from django.urls import reverse, resolve
from tests.BaseTestWithDB import BaseTestWithDB


class UpcomingEventsURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_upcoming_url(self):
        url = reverse("events:upcoming")
        self.assertEqual(url, "/events/upcoming/")

    def test_upcoming_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/upcoming/").view_name, "events:upcoming")
