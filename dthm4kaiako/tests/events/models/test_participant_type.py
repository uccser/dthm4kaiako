"""Unit tests for participant type model"""

from events.models import ParticipantType
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
from django.core.exceptions import ValidationError

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class ParticipantTypeTests(BaseTestWithDB):

    # ----------------------------- tests for __str__ ------------------------------

    def test_str_representation__non_free_price(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=10.0
            )
        expected_str = participant_type.name + " ($" + '{0:.2f}'.format(float(participant_type.price)) + ")"
        self.assertEqual(str(participant_type), expected_str)
        
    def test_str_representation__free_one_int_no_dp(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=0
            )
        expected_str = "free"
        self.assertEqual(str(participant_type), expected_str)

            
    def test_str_representation__free_one_int_two_dp(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=0.00
            )
        expected_str = "free"
        self.assertEqual(str(participant_type), expected_str)


    # ----------------------------- tests for is_free ------------------------------

    def test_str_representation__non_free_price(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=10.0
            )
        self.assertFalse(participant_type.is_free())
        
    def test_str_representation__free_one_int_no_dp(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=0
            )
        self.assertTrue(participant_type.is_free())

            
    def test_str_representation__free_one_int_two_dp(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=0.00
            )
        self.assertTrue(participant_type.is_free())

    # ----------------------------- tests for clean ------------------------------

    def test_price_validation_positive_and_one_dp(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=10.0
            )
        try:
            participant_type.full_clean()
        except ValidationError as e:
            self.assertTrue('price' in e.message_dict)

    def test_price_validation_positive_and_zero_dp_and_dot(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=10.
            )
        try:
            participant_type.full_clean()
        except ValidationError as e:
            self.assertTrue('price' in e.message_dict)

    
    def test_price_validation_positive_and_three_dp(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=10.000
            )
        try:
            participant_type.full_clean()
        except ValidationError as e:
            self.assertTrue('price' in e.message_dict)

    
    def test_price_validation_positive_and_no_leading_int(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=.12
            )
        try:
            participant_type.full_clean()
        except ValidationError as e:
            self.assertTrue('price' in e.message_dict)

    def test_price_validation_negative(self):
        participant_type = ParticipantType.objects.create(
                id=1,
                name="Event staff",
                price=-10.12
            )
        try:
            participant_type.full_clean()
        except ValidationError as e:
            self.assertTrue('price' in e.message_dict)


    def test_price_letters(self):
        with self.assertRaises(ValueError):
            ParticipantType.objects.create(
                    id=1,
                    name="Event staff",
                    price="abc"
                )