"""Unit tests for address"""

from django.test import TestCase
from events.models import Address, EventRegistration
from tests.dthm4kaiako_test_data_generator import (
    generate_addresses
)
import pytz

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')
from tests.BaseTestWithDB import BaseTestWithDB


class AddressTests(BaseTestWithDB):

    @classmethod
    def setUpTestData(cls):
        generate_addresses()

    @classmethod
    def tearDownTestData(cls):
        Address.objects.all().delete()

    # ------------------------------- tests for __str__ ----------------------------

    def test_str_representation(self):
        registration = EventRegistration.objects.get(id=1)
        billing_address = registration.billing_physical_address
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
        registration = EventRegistration.objects.get(id=1)
        billing_address = registration.billing_physical_address
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
