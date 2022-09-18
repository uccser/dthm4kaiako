# from http import HTTPStatus
# from django.urls import reverse
# from django.test.utils import override_settings
# from tests.BaseTestWithDB import BaseTestWithDB

# TODO: fix me
# class EventApplicationsViewTest(BaseTestWithDB):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.language = "en"

#     @override_settings(GOOGLE_MAPS_API_KEY="mocked")
#     def test_event_applications_view_success_response(self):
#         response = self.client.get(reverse("events:event_applications"))
#         self.assertEqual(HTTPStatus.OK, response.status_code)
