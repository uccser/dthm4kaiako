"""Unit tests for events"""

import pytest
from django.test import TestCase
from events.models import (
    Event, 
    ApplicantType,
    Address,
    EventApplication,
    )

pytestmark = pytest.mark.django_db

class EventModelTests(TestCase):

    # ----------------------- tests for is_register_or_apply -----------------------

    def test_is_register_or_apply__event_is_register(self):
        pass 

    def test_is_register_or_apply__event_is_apply(self):
        pass 
        
    def test_is_register_or_apply__event_is_neither(self):
        pass 

    # ---------------------------- tests for has_ended ----------------------------

    def test_has_ended__event_ended(self):
        pass 

    def test_has_ended__event_has_not_ended(self):
        pass 

    # ------------------------ tests for has_attendance_fee -----------------------
    def test_has_attendance_fee__event_has_fee(self):
        pass 

    def test_has_attendance_fee__event_is_free(self):
        pass 


class ApplicantTypeTests(TestCase):

    # ----------------------------- tests for __str__ ------------------------------

    def test_str_representation(self):
        pass 


class AddressTests(TestCase):

    # ------------------------------- tests for __str__ ----------------------------

    def test_str_representation(self):
        pass 

    # ---------------------------- tests for get_full_address ----------------------

    def test_get_full_address(self):
        pass 


class EventApplicationTests(TestCase):

    # ------------------------------- tests for status_string_for_user ----------------------------

    def test_status_string_for_user__pending(self):
        pass 

    def test_status_string_for_user__approved(self):
        pass 

    def test_status_string_for_user__rejected(self):
        pass 

    def test_status_string_for_user__withdrawn(self):
        pass 

    
    # ------------------------------- tests for withdraw ------------------------------

    def test_withdraw__not_already_withdrawn(self):
        pass 

    def test_withdraw__already_withdrawn(self):
        pass 

    
    # ------------------------------- tests for get_absolute_url ------------------------------

    def test_get_absolute_url(self):
        pass 
