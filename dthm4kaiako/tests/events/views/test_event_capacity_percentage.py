"""Unit tests for event_capacity_percentage."""

from users.models import User
from events.models import (
    Event,
    Address,
    ParticipantType,
    EventRegistration
)
import pytz
from tests.BaseTestWithDB import BaseTestWithDB
import datetime
from events.views import event_capacity_percentage

NEW_ZEALAND_TIME_ZONE = pytz.timezone('Pacific/Auckland')


class EventCapacityPercentageTests(BaseTestWithDB):

    def test_capacity_percentage_capacity(self):
        user_kate = User.objects.create(
            id=1,
            username='kate',
            first_name='Kate',
            last_name='Bush',
            email='kate@uclive.ac.nz',
            password='potato',
        )
        user_kate.save()

        event_physical_register_1 = Event.objects.create(
            name="DTHM for Kaiako Conference 2023",
            description="description",
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True,
            capacity=10
        )
        event_physical_register_1.save()

        billing_address_1 = Address.objects.create(
            id=1,
            street_number='12',
            street_name='High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14
        )
        billing_address_1.save()

        participant_type = ParticipantType.objects.create(name="Teacher", price=10.00)
        participant_type.save()

        event_registration_1_pending = EventRegistration.objects.create(
            id=1,
            participant_type=participant_type,
            user=user_kate,
            event=event_physical_register_1,
            billing_physical_address=billing_address_1,
            billing_email_address="test@test.co.nz"
        )
        approved = 2
        event_registration_1_pending.status = approved
        event_registration_1_pending.save()

        expected_result = float(10)
        self.assertEqual(event_capacity_percentage(event_physical_register_1), expected_result)
