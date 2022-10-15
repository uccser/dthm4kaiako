"""Unit tests for events home url"""

from django.urls import reverse, resolve
from http import HTTPStatus
from tests.dthm4kaiako_test_data_generator import generate_users
from tests.BaseTestWithDB import BaseTestWithDB
from django.test.utils import override_settings
from users.models import User


class HomeURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        User.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_home_reverse_provides_correct_url(self):
        url = reverse("events:home")
        self.assertEqual(url, "/events/")

    def test_home_resolve_provides_correct_view_name(self):
        self.assertEqual(resolve("/events/").view_name, "events:home")

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_home_gives_200_status_code(self):
        user = User.objects.create_user(
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user.save()
        self.client.force_login(user)
        url = reverse("events:home")
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
