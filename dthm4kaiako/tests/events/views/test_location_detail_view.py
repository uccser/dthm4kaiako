"""Unit tests for location_detail_views"""

from tests.BaseTestWithDB import BaseTestWithDB
from django.urls import reverse
from http import HTTPStatus
from django.test.utils import override_settings
from events.models import Location
from events.models import (
    Event,
)
import datetime
import pytz
from django.contrib.gis.geos import Point
NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')

class LocationDetailViewTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    @override_settings(GOOGLE_MAPS_API_KEY="mocked")
    def test_location_detail_view_success_response(self):
        location = Location.objects.create(
            room='Room 456',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-12, 149)
        )
        location.save()
        event = Event.objects.create(
            name="Security in CS",
            description="description",
            registration_type=2,
            start=datetime.datetime(2023, 2, 13),
            end=datetime.datetime(2023, 2, 14),
            accessible_online=False,
            published=True
        )
        event.locations.set([location])
        event.save()

        kwargs = {'pk': location.pk}
        response = self.client.get(reverse("events:location", kwargs=kwargs))
        self.assertEqual(HTTPStatus.OK, response.status_code)
