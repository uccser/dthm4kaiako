from django.urls import reverse, resolve
from http import HTTPStatus
from django.test.utils import override_settings
from events.models import Location
from tests.dthm4kaiako_test_data_generator import (
    generate_locations
)
from tests.BaseTestWithDB import BaseTestWithDB


class LocationURLTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_location_url(self):
        generate_locations()
        location = Location.objects.get(pk=1)
        kwargs = {
            'pk': location.pk,
            }
        url = reverse('events:location', kwargs=kwargs)
        expected_url = f"/events/location/{location.pk}/"
        self.assertEqual(url, expected_url)

    # TODO: fix me! - clashing with fourth test
    # def test_location_resolve_provides_correct_view_name(self):
    #     self.assertEqual(resolve("/events/location/").view_name, "events:home")

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_location_url_returns_200_when_object_exists(self):
        generate_locations()
        location = Location.objects.get(pk=1)
        kwargs = {
            'pk': location.pk,
            }
        url = reverse('events:location', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    # ------- Location redirect tests ---------

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_location_redirects_to_home(self):
        response = self.client.get('/events/location/')
        self.assertRedirects(response, '/events/')
