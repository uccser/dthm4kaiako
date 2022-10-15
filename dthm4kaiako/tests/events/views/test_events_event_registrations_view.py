from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from users.models import User
from events.models import (
    Event,
)
import datetime
import pytz
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')

class EventApplicationsViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    # TODO: fix
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_event_registrations_view_success_response(self):
        response = self.client.get(reverse("events:event_registrations"))
        self.assertEqual(HTTPStatus.OK, response.status_code)
