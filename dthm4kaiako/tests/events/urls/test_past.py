"""Unit tests for past events url"""

from django.urls import reverse, resolve
from tests.BaseTestWithDB import BaseTestWithDB


class PastEventsURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_past_url(self):
        self.assertEqual(reverse("events:past"), "/events/past/")

    def test_past_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/past/").view_name, "events:past")
