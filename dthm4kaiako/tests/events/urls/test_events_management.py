"""Unit tests for events_management url"""

from django.urls import reverse, resolve
from http import HTTPStatus
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User
from django.test.utils import override_settings


class EventsManagementURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_events_management_url(self):
        url = reverse('events:events_management')
        expected_url = "/events/manage/"
        self.assertEqual(url, expected_url)

    def test_events_management_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/manage/").view_name, "events:events_management")

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
