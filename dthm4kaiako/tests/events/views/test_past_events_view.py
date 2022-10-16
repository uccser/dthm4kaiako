from http import HTTPStatus
from django.urls import reverse
from django.test.utils import override_settings
from tests.BaseTestWithDB import BaseTestWithDB
import pytz
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventPastViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_past_gives_200_status_code(self):
        url = reverse("events:past")
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertContains(response, "Events")
