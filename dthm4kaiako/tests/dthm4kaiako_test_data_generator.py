"""Class to generate test data required for testing dthm4kaiako system."""

from django.contrib.auth import get_user_model
import datetime
from users.models import DietaryRequirement
from events.models import (
    Location,
    Series,
    Event,
    Session,
    Address,
    EventRegistration,
    RegistrationForm,
)
from django.contrib.gis.geos import Point


User = get_user_model()


def generate_dietary_requirements():
    """Generate dietary requirements for use in dthm4kaiako tests."""
    dietary_requirement_none = DietaryRequirement.objects.create(
        id=1,
        name="None"
        )
    dietary_requirement_diary_free = DietaryRequirement.objects.create(
        id=2,
        name="Dairy free"
        )
    dietary_requirement_gluten_free = DietaryRequirement.objects.create(
        id=3,
        name="Gluten free"
        )
    dietary_requirement_vegetarian = DietaryRequirement.objects.create(
        id=4,
        name="Vegetarian"
        )
    dietary_requirement_vegan = DietaryRequirement.objects.create(
        id=5,
        name="Vegan"
        )
    dietary_requirement_paleo = DietaryRequirement.objects.create(
        id=6,
        name="Paleo"
        )
    dietary_requirement_fodmap = DietaryRequirement.objects.create(
        id=7,
        name="FODMAP"
        )
    dietary_requirement_nut_allergies = DietaryRequirement.objects.create(
        id=8,
        name="Nut allergies"
        )
    dietary_requirement_seafood_allergies = DietaryRequirement.objects.create(
        id=9,
        name="Fish and shellfish allergies"
        )
    dietary_requirement_keto = DietaryRequirement.objects.create(
        id=10,
        name="Keto"
        )
    dietary_requirement_halal = DietaryRequirement.objects.create(
        id=11,
        name="Halal"
        )
    dietary_requirement_coffee = DietaryRequirement.objects.create(
        id=12,
        name="As long as there's coffee, I'm happy!"
        )

    dietary_requirement_none.save()
    dietary_requirement_diary_free.save()
    dietary_requirement_gluten_free.save()
    dietary_requirement_vegetarian.save()
    dietary_requirement_vegan.save()
    dietary_requirement_paleo.save()
    dietary_requirement_fodmap.save()
    dietary_requirement_nut_allergies.save()
    dietary_requirement_seafood_allergies.save()
    dietary_requirement_keto.save()
    dietary_requirement_halal.save()
    dietary_requirement_coffee.save()


def generate_addresses():
    """Generate billing addresses for use in dthm4kaiako tests."""
    billing_address_1 = Address.objects.create(
        id=1,
        street_number='12',
        street_name='High Street',
        suburb='Riccarton',
        city='Chrirstchurch',
        region=14
    )
    billing_address_1.save()


def generate_users():
    """Generate users for dthm4kaiako tests. Creates multiple basic users for unit tests."""
    user_kate = User.objects.create_user(
        id=1,
        username='kate',
        first_name='Kate',
        last_name='Bush',
        email='kate@uclive.ac.nz',
        password='potato',
    )
    user_kate.save()

    user_fiona = User.objects.create_user(
        id=2,
        username='fiona',
        first_name='Fiona',
        last_name='Apple',
        email='fiona@uclive.ac.nz',
        password='potato',
    )
    user_fiona.save()

    user_tori = User.objects.create_user(
        id=3,
        username='tori',
        first_name='Tori',
        last_name='Amos',
        email='tori@uclive.ac.nz',
        password='potato',
    )
    user_tori.save()


def generate_entities():
    """Generate entities for use in dthm4kaiako tests."""
    pass


def generate_locations():
    """Generate locations for use in dthm4kaiako tests."""
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

    location_2 = Location.objects.create(
        id=2,
        room='Room 456',
        name='Middleton Grange School',
        street_address='12 High Street',
        suburb='Riccarton',
        city='Chrirstchurch',
        region=14,
        coords=Point(-12, 149)
    )
    location_2.save()

    location_3 = Location.objects.create(
        id=3,
        room='Room 7',
        name='Middleton Grange School',
        street_address='12 High Street',
        suburb='Riccarton',
        city='Chrirstchurch',
        region=14,
        coords=Point(-27, 188)
    )
    location_3.save()


def generate_serieses():
    """Generate serieses for use in dthm4kaiako tests."""
    series_1 = Series.objects.create(
        id=1,
        name='Artificial Intelligence series',
        abbreviation='AI series',
        description='Some description',
    )
    series_1.save()


def generate_events():
    """Generate events for use in dthm4kaiako tests."""
    location_1 = Location.objects.get(id=1)
    location_2 = Location.objects.get(id=2)
    location_3 = Location.objects.get(id=3)

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

    event_physical_apply_1 = Event.objects.create(
        id=2,
        name="Security in CS",
        description="description",
        registration_type=2,
        start=datetime.date(2023, 2, 13),
        end=datetime.date(2023, 2, 14),
        accessible_online=False,
        published=True
    )
    event_physical_apply_1.locations.set([location_2, location_3])
    event_physical_apply_1.save()

    event_physical_invite_1 = Event.objects.create(
        id=3,
        name="Teaching with AI",
        description="description",
        registration_type=4,
        start=datetime.date(2023, 4, 15),
        end=datetime.date(2023, 4, 15),
        accessible_online=False,
        # locations = location_3,
        series=Series.objects.get(name='Artificial Intelligence series'),
        published=True
    )
    event_physical_invite_1.save()

    event_ended_1 = Event.objects.create(
        id=4,
        name="Teaching with AI",
        description="description",
        registration_type=4,
        start=datetime.date(2020, 4, 15),
        end=datetime.date(2020, 4, 15),
        accessible_online=False,
        # locations = location_3,
        series=Series.objects.get(name='Artificial Intelligence series'),
        published=True
    )
    event_ended_1.save()

    event_physical_register_2 = Event.objects.create(
        id=5,
        name="Intro to logic gates",
        description="description",
        registration_type=1,
        start=datetime.date(2023, 1, 24),
        end=datetime.date(2023, 1, 26),
        accessible_online=False,
        published=True
    )
    event_physical_register_2.save()

    event_physical_register_3 = Event.objects.create(
        id=6,
        name="Cryptocurrency - what is it?",
        description="description",
        registration_type=1,
        start=datetime.date(2023, 4, 3),
        end=datetime.date(2023, 4, 10),
        accessible_online=False,
        published=True
    )
    event_physical_register_3.save()

    event_physical_register_4 = Event.objects.create(
        id=7,
        name="Resource jam!",
        description="description",
        registration_type=1,
        start=datetime.date(2023, 2, 28),
        end=datetime.date(2023, 3, 3),
        accessible_online=False,
        published=True
    )
    event_physical_register_4.save()

    event_online_register_1 = Event.objects.create(
        id=8,
        name="Zoom for Beginners",
        description="description",
        registration_type=1,
        start=datetime.date(2023, 2, 14),
        end=datetime.date(2023, 3, 14),
        accessible_online=True,
        published=True
    )
    event_online_register_1.save()


def generate_sessions():
    """Generate sessions for use in dthm4kaiako tests."""
    # session_2_event_1
    Session.objects.create(
        id=1,
        name="session 2",
        description="some description",
        start=datetime.datetime(2023, 6, 24, 13, 0, 0),
        end=datetime.datetime(2023, 6, 24, 16, 0, 0),
        event=Event.objects.get(id=1),
    )

    # session_1_event_1
    Session.objects.create(
        id=2,
        name="session 1",
        description="some description",
        start=datetime.datetime(2023, 6, 24, 9, 0, 0),
        end=datetime.datetime(2023, 6, 24, 12, 0, 0),
        event=Event.objects.get(id=1),
    )

    # session_1_event_2
    Session.objects.create(
        id=3,
        name="session 1",
        description="some description",
        start=datetime.datetime(2023, 2, 13, 10, 30, 0),
        end=datetime.datetime(2023, 2, 13, 12, 30, 0),
        event=Event.objects.get(id=2),
    )

    # session_2_event_2
    Session.objects.create(
        id=4,
        name="session 2",
        description="some description",
        start=datetime.datetime(2023, 2, 13, 10, 30, 0),
        end=datetime.datetime(2023, 2, 13, 12, 30, 0),
        event=Event.objects.get(id=2),
    )

    # session_1_event_3
    Session.objects.create(
        id=5,
        name="session 1",
        description="some description",
        start=datetime.datetime(2023, 2, 13, 10, 30, 0),
        end=datetime.datetime(2023, 2, 13, 12, 30, 0),
        event=Event.objects.get(id=3),
    )

    # session_2_event_3
    Session.objects.create(
        id=6,
        name="session 2",
        description="some description",
        start=datetime.datetime(2023, 2, 13, 10, 30, 0),
        end=datetime.datetime(2023, 2, 14, 12, 30, 0),
        event=Event.objects.get(id=3),
    )

    # session_1_event_4
    Session.objects.create(
        id=7,
        name="session 1",
        description="some description",
        start=datetime.datetime(2020, 4, 15, 10, 30, 0),
        end=datetime.datetime(2020, 4, 15, 12, 30, 0),
        event=Event.objects.get(id=4),
    )

    # session_2_event_4
    Session.objects.create(
        id=8,
        name="session 2",
        description="some description",
        start=datetime.datetime(2020, 4, 16, 10, 30, 0),
        end=datetime.datetime(2020, 4, 16, 12, 30, 0),
        event=Event.objects.get(id=4),
    )

    # session_3_event_4
    Session.objects.create(
        id=9,
        name="session 3",
        description="some description",
        start=datetime.datetime(2020, 4, 16, 10, 30, 0),
        end=datetime.datetime(2020, 4, 16, 12, 30, 0),
        event=Event.objects.get(id=4),
    )

    # session_3_event_5
    Session.objects.create(
        id=12,
        name="session 3",
        description="some description",
        start=datetime.datetime(2023, 1, 26, 11, 30, 0),
        end=datetime.datetime(2023, 1, 26, 15, 30, 0),
        event=Event.objects.get(id=5),
    )

    # session_4_event_5
    Session.objects.create(
        id=13,
        name="session 4",
        description="some description",
        start=datetime.datetime(2023, 1, 27, 14, 30, 0),
        end=datetime.datetime(2023, 1, 27, 16, 30, 0),
        event=Event.objects.get(id=5),
    )

    # session_1_event_5
    Session.objects.create(
        id=10,
        name="session 1",
        description="some description",
        start=datetime.datetime(2023, 1, 24, 13, 30, 0),
        end=datetime.datetime(2023, 1, 24, 17, 30, 0),
        event=Event.objects.get(id=5),
    )

    # session_2_event_5
    Session.objects.create(
        id=11,
        name="session 2",
        description="some description",
        start=datetime.datetime(2023, 1, 25, 9, 30, 0),
        end=datetime.datetime(2023, 1, 25, 13, 30, 0),
        event=Event.objects.get(id=5),
    )

    # session_3_event_6
    Session.objects.create(
        id=14,
        name="session 3",
        description="some description",
        start=datetime.datetime(2023, 4, 3, 11, 30, 0),
        end=datetime.datetime(2023, 1, 26, 12, 30, 0),
        event=Event.objects.get(id=6),
    )

    # session_4_event_6
    Session.objects.create(
        id=15,
        name="session 4",
        start=datetime.datetime(2023, 4, 3, 12, 30, 0),
        end=datetime.datetime(2023, 1, 26, 13, 30, 0),
        event=Event.objects.get(id=6),
    )

    # session_1_event_6
    Session.objects.create(
        id=16,
        name="session 1",
        description="some description",
        start=datetime.datetime(2023, 4, 3, 9, 30, 0),
        end=datetime.datetime(2023, 1, 26, 10, 30, 0),
        event=Event.objects.get(id=6),
    )

    # session_2_event_6
    Session.objects.create(
        id=17,
        name="session 2",
        description="some description",
        start=datetime.datetime(2023, 4, 3, 10, 30, 0),
        end=datetime.datetime(2023, 1, 26, 11, 30, 0),
        event=Event.objects.get(id=6),
    )

    # session_3_event_7
    Session.objects.create(
        id=18,
        name="session 3",
        start=datetime.datetime(2023, 3, 2, 14, 0, 0),
        end=datetime.datetime(2023, 3, 2, 16, 0, 0),
        event=Event.objects.get(id=7),
    )

    # session_1_event_7
    Session.objects.create(
        id=19,
        name="session 1",
        description="some description",
        start=datetime.datetime(2023, 2, 28, 14, 0, 0),
        end=datetime.datetime(2023, 2, 28, 16, 0, 0),
        event=Event.objects.get(id=7),
    )

    # session_2_event_7
    Session.objects.create(
        id=20,
        name="session 2",
        description="some description",
        start=datetime.datetime(2023, 3, 1, 14, 0, 0),
        end=datetime.datetime(2023, 3, 1, 16, 0, 0),
        event=Event.objects.get(id=7),
    )

# TODO: update to tickets
# def generate_participant_types():
#     """Generate participant types for use in dthm4kaiako tests."""
#     registration_type_event_staff = ParticipantType.objects.create(
#         id=1,
#         name="Event staff"
#         )
#     registration_type_event_staff.save()

#     registration_type_teacher = ParticipantType.objects.create(
#         id=2,
#         name="Teacher"
#         )
#     registration_type_teacher.save()

#     registration_type_student = ParticipantType.objects.create(
#         id=3,
#         name="Student"
#         )
#     registration_type_student.save()

#     registration_type_student = ParticipantType.objects.create(
#         id=4,
#         name="Facilitator"
#         )
#     registration_type_student.save()


def generate_event_registrations():
    """Generate event registrations for use in dthm4kaiako tests."""
    event_registration_1_pending = EventRegistration.objects.create(
        id=1,
        # participant_type=ParticipantType.objects.get(name="Teacher"),
        user=User.objects.get(id=1),
        event=Event.objects.get(id=1),
        billing_physical_address=Address.objects.get(id=1),
        billing_email_address="test@test.co.nz"
    )
    event_registration_1_pending.status = 1
    event_registration_1_pending.save()

    event_registration_2_approved = EventRegistration.objects.create(
        id=2,
        # participant_type=ParticipantType.objects.get(name="Teacher"),
        user=User.objects.get(id=2),
        event=Event.objects.get(id=1),
        billing_physical_address=Address.objects.get(id=1),
        billing_email_address="test@test.co.nz"
    )
    event_registration_2_approved.status = 2
    event_registration_2_approved.save()

    event_registration_3_declined = EventRegistration.objects.create(
        id=3,
        # participant_type=ParticipantType.objects.get(name="Teacher"),
        user=User.objects.get(id=3),
        event=Event.objects.get(id=1),
        billing_physical_address=Address.objects.get(id=1),
        billing_email_address="test@test.co.nz"
    )
    event_registration_3_declined.status = 3
    event_registration_3_declined.save()


def generate_event_registration_forms():
    """Generate event registration forms for use in dthm4kaiako tests."""
    RegistrationForm.objects.filter(event_id=1).update(
        open_datetime=datetime.date(2022, 1, 1),
        close_datetime=datetime.date(2023, 6, 1),
        terms_and_conditions="Some terms and conditions.",
    )

    RegistrationForm.objects.filter(event_id=2).update(
        open_datetime=datetime.date(2022, 1, 2),
        close_datetime=datetime.date(2023, 2, 1),
        terms_and_conditions="Some terms and conditions.",
    )
