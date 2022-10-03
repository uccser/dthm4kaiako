from django.urls import reverse, resolve
from http import HTTPStatus
from django.test.utils import override_settings
from tests.BaseTestWithDB import BaseTestWithDB


class PastEventsURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_past_url(self):
        self.assertEqual(reverse("events:past"), "/events/past/")

    def test_past_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/past/").view_name, "events:past")

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_past_gives_200_status_code(self):
        url = reverse("events:past")
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)