from django.test import TestCase
from django.contrib.auth.models import User
from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings


class EventDetailViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    @override_settings(GOOGLE_MAPS_API_KEY="mocked") 
    def test_event_detail_view_success_response(self):
        kwargs = {'pk' : 1}
        response = self.client.get(reverse("events:apply", kwargs=kwargs))
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
