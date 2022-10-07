from django.urls import reverse, resolve
from http import HTTPStatus
from tests.dthm4kaiako_test_data_generator import generate_users
from tests.BaseTestWithDB import BaseTestWithDB
from django.test.utils import override_settings
from users.models import User


class HomeURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_home_reverse_provides_correct_url(self):
        url = reverse("events:home")
        self.assertEqual(url, "/events/")

    def test_home_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/").view_name, "events:home")

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_home_gives_200_status_code(self):
        generate_users()
        self.client.force_login(User.objects.get(id=1))
        url = reverse("events:home")
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
