"""Unit tests for events location url"""

from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from events.models import Location
from tests.BaseTestWithDB import BaseTestWithDB
from django.contrib.gis.geos import Point


class LocationURLTest(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Location.objects.all().delete()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_valid_location_url(self):
        location = Location.objects.create(
            id=1,
            room='Room 123',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-43, 172)
        )
        location.save()
        kwargs = {
            'pk': location.pk,
            }
        url = reverse('events:location', kwargs=kwargs)
        expected_url = f"/events/location/{location.pk}/"
        self.assertEqual(url, expected_url)

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_location_url_returns_200_when_object_exists(self):
        location = Location.objects.create(
            id=1,
            room='Room 123',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-43, 172)
        )
        location.save()
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
