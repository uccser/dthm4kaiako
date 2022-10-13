"""Unit tests for address"""

from events.models import (
    Location,
    Address,
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
from django.contrib.gis.geos import Point

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')
from tests.BaseTestWithDB import BaseTestWithDB


class AddressTests(BaseTestWithDB):

    # ------------------------------- tests for __str__ ----------------------------

    def test_str_representation(self):
        billing_address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address.save()
        self.assertEqual(
        str(billing_address),
        '{} {},\n{},\n{},\n{}'.format(
            billing_address.street_number,
            billing_address.street_name,
            billing_address.suburb,
            billing_address.city,
            billing_address.post_code
        )
    )

    # ---------------------------- tests for get_full_address ----------------------

    def test_get_full_address(self):
        billing_address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address.save()
        self.assertEqual(
            str(billing_address.get_full_address()),
            '{} {},\n{},\n{},\n{}'.format(
                billing_address.street_number,
                billing_address.street_name,
                billing_address.suburb,
                billing_address.city,
                billing_address.post_code
            )
        )
