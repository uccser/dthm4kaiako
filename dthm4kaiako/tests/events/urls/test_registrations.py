"""Unit tests for registrations url"""

from django.urls import reverse, resolve
from tests.BaseTestWithDB import BaseTestWithDB


class RegistrationsURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_registrations_url(self):
        url = reverse("events:event_registrations")
        self.assertEqual(url, "/events/registrations/")

    def test_registrations_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/registrations/").view_name, "events:event_registrations")
