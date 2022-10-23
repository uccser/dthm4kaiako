"""Unit tests for events_upcoming_views"""

from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
import pytz
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventsUpcomingViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_upcoming_gives_200_status_code(self):
        url = reverse("events:upcoming")
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertContains(response, "Events")
