"""Unit tests for address"""

from events.models import (
    Location,
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
from django.contrib.gis.geos import Point

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class LocationTests(BaseTestWithDB):

    # ------------------------------- tests for __str__ ----------------------------

    def test_str_representation(self):
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
        self.assertEqual(
            str(location),
            '{},\n{},\n{},\n{}, {},\n{}'.format(
                location.room,
                location.name,
                location.street_address,
                location.suburb,
                location.city,
                location.get_region_display()
            )
        )

    # ---------------------------- tests for get_full_address ----------------------

    def test_get_full_address(self):
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

        self.assertEqual(
            str(location.get_full_address()),
            '{},\n{},\n{},\n{}, {},\n{}'.format(
                location.room,
                location.name,
                location.street_address,
                location.suburb,
                location.city,
                location.get_region_display()
            )
        )
