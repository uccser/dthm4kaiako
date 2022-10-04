"""Unit tests for address"""

from django.test import TestCase
from events.models import Address, EventRegistration
from tests.dthm4kaiako_test_data_generator import (
    generate_addresses
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class AddressTests(BaseTestWithDB):

    @classmethod
    def setUpTestData(cls):
        generate_addresses()

    @classmethod
    def tearDownTestData(cls):
        Address.objects.all().delete()

    # ------------------------------- tests for __str__ ----------------------------
    # TODO
