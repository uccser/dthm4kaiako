"""Unit tests for address"""

from django.test import TestCase
from events.models import Address, EventRegistration
from tests.dthm4kaiako_test_data_generator import (
    generate_addresses
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class LocationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_locations()

    @classmethod
    def tearDownTestData(cls):
        Location.objects.all().delete()

    # ------------------------------- tests for __str__ ----------------------------

    def test_str_representation(self):
        location = Location.objects.get(id=1)
        self.assertEqual(
            str(location),
            '{} {},\n{},\n{},\n{}'.format(
                location.street_number,
                location.street_name,
                location.suburb,
                location.city,
                location.post_code
            )
        )

    # ---------------------------- tests for get_full_address ----------------------

    def test_get_full_address(self):
        location = Location.objects.get(id=1)
        self.assertEqual(
            str(billing_address.get_full_address()),
            '{} {},\n{},\n{},\n{}'.format(
                location.street_number,
                location.street_name,
                location.suburb,
                location.city,
                location.post_code
            )
        )
