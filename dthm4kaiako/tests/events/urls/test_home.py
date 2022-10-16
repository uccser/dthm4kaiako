"""Unit tests for events home url"""

from django.urls import reverse, resolve
from tests.BaseTestWithDB import BaseTestWithDB


class HomeURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_home_reverse_provides_correct_url(self):
        url = reverse("events:home")
        self.assertEqual(url, "/events/")

    def test_home_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/").view_name, "events:home")
