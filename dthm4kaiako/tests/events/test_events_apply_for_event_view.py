from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings


class ApplyForEventViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    # TODO: fix - giving 302 instead of 200
    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_register_for_event_view_redirect_response(self):
        kwargs = {'pk': 1}
        response = self.client.get(reverse("events:register", kwargs=kwargs))
        self.assertEqual(HTTPStatus.FOUND, response.status_code) # redirect to event management page
