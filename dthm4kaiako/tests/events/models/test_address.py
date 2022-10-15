"""Unit tests for address model"""

from events.models import (
    Address
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

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

    # ---------------------------- tests for clean ----------------------

    def test_clean_three_digit_post_code_throws_validation_error(self):
        address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            post_code = 123
        )
        try:
            address.full_clean()
        except ValidationError as e:
            expected = {
                'post_code': 'Post code must be four digits.'
            }
            self.assertTrue(e.message_dict, expected)

    def test_clean_five_digit_post_code_throws_validation_error(self):
        address = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            post_code = 12345
        )
        try:
            address.full_clean()
        except ValidationError as e:
            expected = {
                'post_code': 'Post code must be four digits.'
            }
            self.assertTrue(e.message_dict, expected)
    
    def test_clean_spaces_in_street_number_throws_validation_error(self):
        address = Address.objects.create(
            id=1,
            street_number=' ',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            post_code = 12345
        )
        try:
            address.full_clean()
        except ValidationError as e:
            expected = {
                'street_number': 'Street number can only include upper and lower case letters and numbers.'
            }
            self.assertTrue(e.message_dict, expected)
