"""Unit tests for registration"""

from django.test import TestCase
from django.contrib.auth.models import User
from events.models import Address, EventRegistration
from tests.dthm4kaiako_test_data_generator import (
    generate_addresses
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventRegistrationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_addresses()
        generate_serieses()
        generate_locations()
        generate_events()
        generate_users()
        # generate_participant_types()
        generate_event_registrations()

    @classmethod
    def tearDownTestData(cls):
        Address.objects.all().delete()
        Series.objects.all().delete()
        Location.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()
        # ParticipantType.objects.all().delete()
        EventRegistration.objects.all().delete()


    # ------------------------------- tests for __str__ ----------------------------
    # TODO

    # ------------------------------- tests for status_string_for_user ----------------------------

    def test_status_string_for_user__pending(self):
        event_registration = EventRegistration.objects.get(id=1)
        self.assertEqual(event_registration.status_string_for_user, "Pending")

    def test_status_string_for_user__approved(self):
        event_registration = EventRegistration.objects.get(id=2)
        self.assertEqual(event_registration.status_string_for_user, "Approved")

    def test_status_string_for_user__declined(self):
        event_registration = EventRegistration.objects.get(id=3)
        self.assertEqual(event_registration.status_string_for_user, "Declined")
