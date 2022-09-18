# from tests.BaseTestWithDB import BaseTestWithDB
# from django.urls import reverse
# from http import HTTPStatus
# from django.test.utils import override_settings
# from events.models import Location
# from unittest import mock


# TODO: fix me
# class LocationDetailViewTest(BaseTestWithDB):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.language = "en"

#     # TODO: figure out how to mock that location exists
#     @override_settings(GOOGLE_MAPS_API_KEY="mocked")
#     # @patch('events.models.Location.objects')
#     def test_location_detail_view_success_response(self):
#         location = mock.Mock(spec=Location)
#         location._state = mock.Mock()
#         location.id = 1
#         kwargs = {'pk': 1}
#         response = self.client.get(reverse("events:location", kwargs=kwargs))
#         self.assertEqual(HTTPStatus.OK, response.status_code)
