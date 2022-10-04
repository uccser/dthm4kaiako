"""Unit tests for registration form"""

from django.test import TestCase
from django.contrib.auth.models import User
from events.models import (
    Event,
    Address,
    EventRegistration,
    Series,
    Location,
    RegistrationForm
    )
from tests.dthm4kaiako_test_data_generator import (
    generate_locations,
    generate_users,
    generate_events,
    generate_addresses,
    generate_event_registrations,
    generate_serieses,
)
from unittest import mock
import datetime
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class RegistrationFormTests(TestCase):

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

    # ------------------------------- tests for get_absolute_url ------------------------------

    def test_get_absolute_url__returns_url_of_registration_form_on_website(self):
        reg_form = RegistrationForm.objects.get(event_id=1)
        event = reg_form.event
        event_pk = event.pk
        expected_url = '/events/register/{}/'.format(event_pk)
        self.assertEqual(str(reg_form.get_absolute_url()), expected_url)
