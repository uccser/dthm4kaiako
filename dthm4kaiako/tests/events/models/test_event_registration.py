"""Unit tests for event registration model"""

from django.contrib.auth import get_user_model
from events.models import (
    Event,
    EventRegistration,
    ParticipantType,
    Address,
    Location,
)
from django.contrib.gis.geos import Point
import datetime
import pytz
from tests.BaseTestWithDB import BaseTestWithDB

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')
User = get_user_model()


class EventRegistrationTests(BaseTestWithDB):

    @classmethod
    def tearDownTestData(cls):
        Event.objects.all().delete()
        EventRegistration.objects.all().delete()
        ParticipantType.objects.all().delete()
        Location.objects.all().delete()
        Address.objects.all().delete()

    # ------------------------------- tests for __str__ ----------------------------
    def test_event_registration_str(self):
        user_kate = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

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

        billing_address_1 = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address_1.save()

        event_registration_1_pending = EventRegistration.objects.create(
            id=1,
            participant_type=participant_type,
            user=user_kate,
            event=Event.objects.get(id=1),
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz"
        )
        event_registration_1_pending.status = 1
        event_registration_1_pending.save()

        expected = event_registration_1_pending.user.first_name + " " + event_registration_1_pending.user.last_name

        self.assertEqual(str(event_registration_1_pending), expected)

    # ------------------------------- tests for status_string_for_user ----------------------------

    def test_status_string_for_user__pending(self):
        user_kate = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

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

        billing_address_1 = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address_1.save()

        event_registration_1_pending = EventRegistration.objects.create(
            id=1,
            participant_type=participant_type,
            user=user_kate,
            event=Event.objects.get(id=1),
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz"
        )
        event_registration_1_pending.status = 1
        event_registration_1_pending.save()

        event_registration = EventRegistration.objects.get(id=event_registration_1_pending.pk)
        self.assertEqual(event_registration.status_string_for_user, "Pending")

    def test_status_string_for_user__approved(self):
        user_kate = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

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

        billing_address_1 = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address_1.save()

        event_registration_1_pending = EventRegistration.objects.create(
            id=1,
            participant_type=participant_type,
            user=user_kate,
            event=Event.objects.get(id=1),
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz"
        )
        event_registration_1_pending.status = 2
        event_registration_1_pending.save()

        event_registration = EventRegistration.objects.get(id=event_registration_1_pending.pk)
        self.assertEqual(event_registration.status_string_for_user, "Approved")

    def test_status_string_for_user__declined(self):
        user_kate = User.objects.create_user(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

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

        billing_address_1 = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address_1.save()

        event_registration_1_pending = EventRegistration.objects.create(
            id=1,
            participant_type=participant_type,
            user=user_kate,
            event=Event.objects.get(id=1),
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz"
        )
        event_registration_1_pending.status = 3
        event_registration_1_pending.save()

        event_registration = EventRegistration.objects.get(id=event_registration_1_pending.pk)
        self.assertEqual(event_registration.status_string_for_user, "Declined")
