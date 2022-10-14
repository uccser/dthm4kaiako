"""Unit tests for registration form model"""

from xml.dom import ValidationErr
from django.contrib.auth.models import User
from events.models import (
    Event,
    Location,
    RegistrationForm,
    ParticipantType
    )
from django.contrib.gis.geos import Point
import datetime
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
from django.core.exceptions import ValidationError

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class RegistrationFormTests(BaseTestWithDB):

    # ------------------------------- tests for get_absolute_url ------------------------------

    def test_get_absolute_url__returns_url_of_registration_form_on_website(self):
        location_1 = Location.objects.create(
            id=1,
            room='Room 123',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-43, 172)
        )
        location_1.save()

        event_physical_register_1 = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event_physical_register_1.locations.set([location_1])
        event_physical_register_1.save()

        participant_type = ParticipantType.objects.create(name="Teacher", price=10.00)
        participant_type.save()
        event_physical_register_1.participant_types.set([participant_type])

        reg_form = event_physical_register_1.registration_form

        event_pk = event_physical_register_1.pk
        expected_url = '/events/register/{}/'.format(event_pk)
        self.assertEqual(str(reg_form.get_absolute_url()), expected_url)


    # ------------------------------- tests for clean ------------------------------

    def test_clean_reg_form_exists_for_event_already_throw_validation_error(self):
        location_1 = Location.objects.create(
            id=1,
            room='Room 123',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-43, 172)
        )
        location_1.save()

        event_physical_register_1 = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event_physical_register_1.locations.set([location_1])
        event_physical_register_1.save()

        participant_type = ParticipantType.objects.create(name="Teacher", price=10.00)
        participant_type.save()
        event_physical_register_1.participant_types.set([participant_type])

        try:
            RegistrationForm.objects.create(
                open_datetime=datetime.date(2022, 1, 1),
                close_datetime=datetime.date(2023, 6, 1),
                terms_and_conditions="Some terms and conditions.",
                event = event_physical_register_1,
            )
        except ValidationError as e:
            expected_dict = {'event': ['Registration form with this Event already exists.']}
            self.assertEqual(e.message_dict, expected_dict)


    def test_clean_need_at_least_one_participant_type_for_registrations_to_open_validation_error_thrown(self):
        location_1 = Location.objects.create(
            id=1,
            room='Room 123',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-43, 172)
        )
        location_1.save()

        event_physical_register_1 = Event.objects.create(
            id=1,
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.date(2023, 6, 24),
            end=datetime.date(2023, 6, 26),
            accessible_online=False,
            published=True
        )
        event_physical_register_1.locations.set([location_1])
        event_physical_register_1.save()

        try:
            RegistrationForm.objects.filter(event = event_physical_register_1).update(
                terms_and_conditions="Some terms and conditions."   
            )
        except ValidationError as e:
            expected_dict = {
                'open_datetime': ['At least one participant type is required for registrations to open.']
            }
            self.assertEqual(e.message_dict, expected_dict)
