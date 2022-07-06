"""Class to generate test data required for testing dthm4kaiako system."""

from django.contrib.auth import get_user_model
from allauth.account.admin import EmailAddress
from django.core import management
import datetime
from users.models import (
    DietaryRequirement,
    User,
    Entity
)
from events.models import (
    Location,
    Series,
    Event, 
    Session,
    ApplicantType,
    Address,
    EventApplication,
    RegistrationForm,
)

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

    pass 
    
    # location_1 = Location.objects.create(
    #     room='Room 123',
    #     name='Middleton Grange School',
    #     street_address='12 High Street',
    #     suburb='Riccarton',
    #     city='Chrirstchurch',
    #     region=14
    # )
    # location_1.save()

    # location_2 = Location.objects.create(
    #     room='Room 456',
    #     name='Middleton Grange School',
    #     street_address='12 High Street',
    #     suburb='Riccarton',
    #     city='Chrirstchurch',
    #     region=14
    # )
    # location_2.save()

    # location_3 = Location.objects.create(
    #     room='Room 7',
    #     name='Middleton Grange School',
    #     street_address='12 High Street',
    #     suburb='Riccarton',
    #     city='Chrirstchurch',
    #     region=14
    # )
    # location_3.save()
    

def generate_serieses():
    """Generate serieses for use in dthm4kaiako tests."""
    pass 


def generate_events():
    """Generate events for use in dthm4kaiako tests."""

    # location_1 = Locations.objects.get(id=1)
    # location_2 = Locations.objects.get(id=2)
    # location_3 = Locations.objects.get(id=3)

    event_physical_register_1 = Event.objects.create(
        id=1,
        name="DTHM for Kaiako Conference 2023",
        description="description",
        registration_type = 1,
        start=datetime.date(2023, 6, 24),
        end=datetime.date(2023, 6, 26),
        accessible_online=False,
        # locations = location_1,
        price=50
    )
    event_physical_register_1.save()

    event_physical_apply_1 = Event.objects.create(
        id=2,
        name="Security in CS",
        description="description",
        registration_type = 2,
        start=datetime.date(2023, 2, 13),
        end=datetime.date(2023, 2, 14),
        accessible_online=False,
        # locations = location_2,
        price=75
    )
    event_physical_apply_1.save()

    event_physical_invite_1 = Event.objects.create(
        id=3,
        name="Teaching with AI",
        description="description",
        registration_type = 4,
        start=datetime.date(2023, 4, 15),
        end=datetime.date(2023, 4, 15),
        accessible_online=False,
        # locations = location_3,
        price=0
    )
    event_physical_invite_1.save()

    event_ended_1 = Event.objects.create(
        id=4,
        name="Teaching with AI",
        description="description",
        registration_type = 4,
        start=datetime.date(2020, 4, 15),
        end=datetime.date(2020, 4, 15),
        accessible_online=False,
        # locations = location_3,
        price=0
    )
    event_ended_1.save()


def generate_sessions():
    """Generate serieses for use in dthm4kaiako tests."""
    pass 


def generate_applicant_types():
    """Generate applicant types for use in dthm4kaiako tests."""
    application_type_event_staff = ApplicantType.objects.create(
        id=1,
        name="Event staff"
        )
    application_type_event_staff.save()

    application_type_teacher = ApplicantType.objects.create(
        id=2,
        name="Teacher"
        )
    application_type_teacher.save()

    application_type_student = ApplicantType.objects.create(
        id=3,
        name="Student"
        )
    application_type_student.save()


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


def generate_event_applications():
    """Generate event applications for use in dthm4kaiako tests."""
    pass


def generate_event_registration_forms():
    """Generate event registration forms for use in dthm4kaiako tests."""
    
    event_physical_register_1 = Event.objects.get(id=1)
    event_physical_register_2 = Event.objects.get(id=2)

   
    event_1_reg_form = RegistrationForm.objects.create(
        # id=1,
        open_datetime = datetime.date(2022, 1, 1),
        close_datetime = datetime.date(2023, 6, 1),
        terms_and_conditions = "Some terms and conditions.",
        event = event_physical_register_1
    )
    event_1_reg_form.save()

    event_2_reg_form = RegistrationForm.objects.create(
        # id=2,
        open_datetime = datetime.date(2022, 1, 1),
        close_datetime = datetime.date(2023, 2, 1),
        terms_and_conditions = "Some terms and conditions.",
        event = event_physical_register_2
    )
    event_2_reg_form.save()
