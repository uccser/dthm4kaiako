"""Unit tests for address"""

from django.test import TestCase
from events.models import Address, EventRegistration
from tests.dthm4kaiako_test_data_generator import (
    generate_addresses
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class ParticipantTypeTests(BaseTestWithDB):

    @classmethod
    def setUpTestData(cls):
        generate_participant_types()

    @classmethod
    def tearDownTestData(cls):
        ParticipantType.objects.all().delete()

    # ----------------------------- tests for __str__ ------------------------------

    # TODO: update
    def test_str_representation__register(self):
        test_name = "Event staff"
        registration_type = ParticipantType.objects.get(name=test_name)
        self.assertEqual(str(registration_type), registration_type.name)