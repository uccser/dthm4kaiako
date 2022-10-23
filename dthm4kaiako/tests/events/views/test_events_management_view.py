"""Unit tests for events_management_view"""

from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from users.models import User

import pytz
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventRegistrationsViewTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_events_management_returns_200_when_event_exists(self):
        user = User.objects.create_user(
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        self.client.force_login(user)
        url = reverse('events:events_management')
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
