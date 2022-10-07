from django.urls import reverse, resolve
from http import HTTPStatus
from tests.dthm4kaiako_test_data_generator import generate_users
from tests.BaseTestWithDB import BaseTestWithDB
from users.models import User


class EventsManagementURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_events_management_url(self):
        url = reverse('events:events_management')
        expected_url = "/events/manage/"
        self.assertEqual(url, expected_url)

    def test_events_management_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/manage/").view_name, "events:events_management")

    # TODO: fix - giving 302 instead of 200
    def test_events_management_returns_200_when_event_exists(self):
        generate_users()
        self.client.force_login(User.objects.get(id=1))
        url = reverse('events:events_management')
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
