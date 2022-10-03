from django.test import TestCase
from django.urls import reverse, resolve
from http import HTTPStatus
from django.test.utils import override_settings
from tests.BaseTestWithDB import BaseTestWithDB


class UpcomingEventsURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_upcoming_url(self):
        url = reverse("events:upcoming")
        self.assertEqual(url, "/events/upcoming/")

    def test_upcoming_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/upcoming/").view_name, "events:upcoming")

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_upcoming_gives_200_status_code(self):
        url = reverse("events:upcoming")
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
