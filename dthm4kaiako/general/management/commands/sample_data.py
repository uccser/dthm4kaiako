"""Module for the custom Django sample_data command."""

import csv
import random
from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from tests.users.factories import EntityFactory
from resources.models import (
    Language,
    TechnologicalArea,
    ProgressOutcome,
    YearLevel,
    CurriculumLearningArea,
)
from tests.resources.factories import (
    ResourceFactory,
    NZQAStandardFactory,
)
# Users
from users.models import (
    DietaryRequirement,
    Entity,
)
# Events
from events.models import (
    DeletedEventApplication,
    EventApplication,
    Location,
    Series,
    Ticket,
    Event,
)
from tests.events.factories import (
    EventFactory,
)
# DTTA
from tests.dtta.factories import (
    NewsArticleFactory,
    PageFactory,
    ProjectFactory,
    RelatedLinkFactory,
)
# POET
from tests.poet.factories import (
    POETFormResourceFactory,
    POETFormSubmissionFactory,
    POETFormProgressOutcomeGroupFactory,
)
from allauth.account.models import EmailAddress
from utils.new_zealand_regions import REGION_CHOICES
import datetime
from utils.new_zealand_regions import REGION_CHOICES, REGION_CANTERBURY


class Command(management.base.BaseCommand):
    """Required command class for the custom Django sample_data command."""

    help = "Add sample data to database."

    def handle(self, *args, **options):
        """Automatically called when the sample_data command is given."""
        if settings.PRODUCTION_ENVIRONMENT:
            raise management.base.CommandError(
                'This command can only be executed on non-production website or local development.'
            )

        # Clear all data
        management.call_command('flush', interactive=False)
        print('Database wiped.')

        # Create common dietary requirements
        dietary_requirement_none = DietaryRequirement.objects.create(name="None")
        dietary_requirement_dairy_free = DietaryRequirement.objects.create(name="Dairy free")
        dietary_requirement_gluten_free = DietaryRequirement.objects.create(name="Gluten free")
        dietary_requirement_vegetarian = DietaryRequirement.objects.create(name="Vegetarian")
        dietary_requirement_vegan = DietaryRequirement.objects.create(name="Vegan")
        dietary_requirement_keto = DietaryRequirement.objects.create(name="Keto")
        dietary_requirement_FODMAP = DietaryRequirement.objects.create(name="Paleo")
        dietary_requirement_dairy_free = DietaryRequirement.objects.create(name="FODMAP")
        dietary_requirement_halal = DietaryRequirement.objects.create(name="Halal")
        dietary_requirement_coffee = DietaryRequirement.objects.create(name="Give me coffee and no-one gets hurt")
        print('Dietary requirements created.')

        # Create standard ticket types
        ticket_free_event_staff = Ticket.objects.create(name="Event Staff", price=0.0)
        ticket_free_teacher = Ticket.objects.create(name="Teacher", price=0.0)
        ticket_free_student = Ticket.objects.create(name="Student", price=0.0)
        ticket_free_facilitator = Ticket.objects.create(name="Facilitator", price=0.0)
        ticket_paid_event_staff = Ticket.objects.create(name="Event Staff", price=3.0)
        ticket_paid_teacher = Ticket.objects.create(name="Teacher", price=50.0)
        ticket_paid_student = Ticket.objects.create(name="Student", price=20.0)
        ticket_paid_facilitator = Ticket.objects.create(name="Facilitator", price=25.0)
        print('Common tickets created.')

        # Create a selection of entities

        entity_1 = Entity.objects.create(name="Aidanfield Christian School, Christchurch")
        entity_2 = Entity.objects.create(name="Otahuhu College, Auckland")
        entity_3 = Entity.objects.create(name="St Bedes College, Christchurch")
        entity_4 = Entity.objects.create(name="Papanui High School, Christchurch")
        entity_5 = Entity.objects.create(name="Burnside High School, Christchurch")
        entity_6 = Entity.objects.create(name="Avonside Girls' High School, Christchurch")
        entity_7 = Entity.objects.create(name="Villa Maria College, Christchurch")
        entity_8 = Entity.objects.create(name="Christchurch Boys' High School, Christchurch")
        entity_9 = Entity.objects.create(name="Christchurch Girls' High School -Te Kura o Hine Waiora, Christchurch")
        entity_10 = Entity.objects.create(name="Mangakino Area School, Waikato")
        entity_11 = Entity.objects.create(name="Bayfield High School, Dunedin")
        entity_12 = Entity.objects.create(name="Digital Technologies Teachers Aotearoa")
        entity_13 = Entity.objects.create(name="Digital Technologies Hangarau Matihiko")
        entity_14 = Entity.objects.create(name="Ministry of Education")
        print('Random selection of educational entities created.')

        User = get_user_model()

        # TODO: make some non-trivial passwords prior study!

        # Create admin account
        admin = User.objects.create_superuser(
            'admin',
            'admin@dthm4kaiako.ac.nz',
            password="password",
            first_name='Admin',
            last_name='Account'
        )
        EmailAddress.objects.create(
            user=admin,
            email=admin.email,
            primary=True,
            verified=True
        )
        print('Admin created.')


        # Create user accounts

        user_1 = User()
        user_1 = User.objects.create_user(
            'user',
            'user_1@dthm4kaiako.ac.nz',
            password="password",
            first_name='Alex',
            last_name='Doe',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 22 1124 0481'
        )
        EmailAddress.objects.create(
            user=user_1,
            email=user_1.email,
            primary=True,
            verified=True
        )
        user_1_drs = [dietary_requirement_coffee, dietary_requirement_gluten_free]
        user_1.dietary_requirements.set(user_1_drs)
        user_1.save()
        user_1_entities = [entity_1, entity_11]
        user_1.educational_entities.set(user_1_entities)
        user_1.save()

        print('User 1 created.')

        user_2 = User()
        user_2 = User.objects.create_user(
            'user',
            'user_2@dthm4kaiako.ac.nz',
            password="password",
            first_name='John',
            last_name='Doe',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 947 001'
        )
        EmailAddress.objects.create(
            user=user_2,
            email=user_2.email,
            primary=True,
            verified=True
        )
        user_2.dietary_requirements.set([dietary_requirement_coffee])
        user_2.educational_entities.set([entity_2])
        user_2.save()
        print('User 2 created.')

        user_3 = User()
        user_3 = User.objects.create_user(
            'user',
            'user_3@dthm4kaiako.ac.nz',
            password="password",
            first_name='James',
            last_name='Rando',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 22 836 0980'
        )
        EmailAddress.objects.create(
            user=user_3,
            email=user_3.email,
            primary=True,
            verified=True
        )
        user_3.dietary_requirements.set([dietary_requirement_coffee])
        user_3.educational_entities.set([entity_3])
        user_3.save()
        print('User 3 created.')

        user_4 = User()
        user_4 = User.objects.create_user(
            'user',
            'user_4@dthm4kaiako.ac.nz',
            password="password",
            first_name='Jo',
            last_name='Brown',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 28 130 4807'
        )
        EmailAddress.objects.create(
            user=user_4,
            email=user_4.email,
            primary=True,
            verified=True
        )
        user_4.dietary_requirements.set([dietary_requirement_coffee, dietary_requirement_vegan])
        user_4.educational_entities.set([entity_4])
        user_4.save()
        print('User 4 created.')

        user_5 = User()
        user_5 = User.objects.create_user(
            'user',
            'user_5@dthm4kaiako.ac.nz',
            password="password",
            first_name='Paul',
            last_name='Kirsh',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 27 860 8283'
        )
        EmailAddress.objects.create(
            user=user_5,
            email=user_5.email,
            primary=True,
            verified=True
        )
        user_5.dietary_requirements.set([dietary_requirement_halal])
        user_5.educational_entities.set([entity_5])
        user_5.save()
        print('User 5 created.')

        user_6 = User()
        user_6 = User.objects.create_user(
            'user',
            'user_6@dthm4kaiako.ac.nz',
            password="password",
            first_name='Clark',
            last_name='Kent',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 28 8871 3787'
        )
        EmailAddress.objects.create(
            user=user_6,
            email=user_6.email,
            primary=True,
            verified=True
        )
        user_6.dietary_requirements.set([dietary_requirement_keto])
        user_6.educational_entities.set([entity_6])
        user_6.save()
        print('User 6 created.')

        user_7 = User()
        user_7 = User.objects.create_user(
            'user',
            'user_7@dthm4kaiako.ac.nz',
            password="password",
            first_name='Peter',
            last_name='Toddrick',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 877 010'
        )
        EmailAddress.objects.create(
            user=user_7,
            email=user_7.email,
            primary=True,
            verified=True
        )
        user_7.dietary_requirements.set([dietary_requirement_keto])
        user_7.educational_entities.set([entity_7])
        user_7.save()
        print('User 7 created.')

        user_8 = User()
        user_8 = User.objects.create_user(
            'user',
            'user_8@dthm4kaiako.ac.nz',
            password="password",
            first_name='Kate',
            last_name='Pepperson',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 542 958'
        )
        EmailAddress.objects.create(
            user=user_8,
            email=user_8.email,
            primary=True,
            verified=True
        )
        user_8.dietary_requirements.set([dietary_requirement_keto])
        user_8.educational_entities.set([entity_8])
        user_8.save()
        print('User 8 created.')

        user_9 = User()
        user_9 = User.objects.create_user(
            'user',
            'user_9@dthm4kaiako.ac.nz',
            password="password",
            first_name='Kate',
            last_name='Pepperson',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 274 680 498'
        )
        EmailAddress.objects.create(
            user=user_9,
            email=user_9.email,
            primary=True,
            verified=True
        )
        user_9.dietary_requirements.set([dietary_requirement_keto])
        user_9.educational_entities.set([entity_9])
        user_9.save()
        print('User 9 created.')

        user_10 = User()
        user_10 = User.objects.create_user(
            'user',
            'user_10@dthm4kaiako.ac.nz',
            password="password",
            first_name='Scarlett',
            last_name='Jonson',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 942 390'
        )
        EmailAddress.objects.create(
            user=user_10,
            email=user_10.email,
            primary=True,
            verified=True
        )
        user_10.dietary_requirements.set([dietary_requirement_coffee, dietary_requirement_dairy_free])
        user_10.educational_entities.set([entity_7])
        user_10.save()
        print('User 10 created.')

        user_11 = User()
        user_11 = User.objects.create_user(
            'user',
            'user_11@dthm4kaiako.ac.nz',
            password="password",
            first_name='David',
            last_name='Rodder',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 545 878'
        )
        EmailAddress.objects.create(
            user=user_11,
            email=user_11.email,
            primary=True,
            verified=True,
        )
        user_11.dietary_requirements.set([dietary_requirement_coffee, dietary_requirement_vegetarian])
        user_11.educational_entities.set([entity_10])
        user_11.save()
        print('User 11 created.')

        user_12 = User()
        user_12 = User.objects.create_user(
            'user',
            'user_12@dthm4kaiako.ac.nz',
            password="password",
            first_name='Chris',
            last_name='Masters',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 545 878'
        )
        EmailAddress.objects.create(
            user=user_12,
            email=user_12.email,
            primary=True,
            verified=True,
        )
        user_12.dietary_requirements.set([dietary_requirement_FODMAP])
        user_12.educational_entities.set([entity_12, entity_13, entity_14])
        user_12.save()
        print('User 12 created.')

        user_study_participant = User()
        user_study_participant = User.objects.create_user(
            'user',
            'user_study_participant@dthm4kaiako.ac.nz',
            password="password",
            first_name='Study',
            last_name='Participant',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 545 878'
        )
        EmailAddress.objects.create(
            user=user_study_participant,
            email=user_study_participant.email,
            primary=True,
            verified=True
        )
        print('User 13 created.')


        # Physical locations 
        sample_location_1 = Location.objects.create(
          name='University of Canterbury',
          suburb='Ilam',
          city='Christchurch',
          region='14',
          coords=Point(-43, 172)
        )
        sample_location_2 = Location.objects.create(
            room='Room 456',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-12, 149)
        )
        sample_location_3 = Location.objects.create(
            room='Room 7',
            name='Middleton Grange School',
            street_address='12 High Street',
            suburb='Riccarton',
            city='Chrirstchurch',
            region=14,
            coords=Point(-27, 188)
        )
        print('Locations created.')


        # ALL STAFFED BY STUDY PARTICIPANT
        # Event - apply - online
        event_1_apply_online_free_future = Event.objects.create(
            name='DTHM for Kaiako Conference 2021',
            description=(
                'Inspirational collaboration to build your confidence teaching DT & HM.\n\n'
                'This is a FREE face to face Digital Technologies Teachers Aotearoa (DTTA) subject '
                'association event, for all teachers in Aotearoa. It\'s all about building your '
                'practice as a kaiako, for your learners.\n\n'
                'Join us for 3 days of:\n\n'
                'Connecting and reconnecting with colleagues across Aotearoa\n\n'
                'Engaging with a team to uncover and bring to light inspirational learning resources\n\n'
                'Developing programmes of learning that you will confidently take '
                'into your classroom and use immediately',
            ),
            start=datetime.datetime(2023, 4, 23, 8, 0, 0),
            end=datetime.datetime(2023, 4, 23, 11, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            registration_type = 2,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
        )
        event_1_apply_online_free_future.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_1_apply_online_free_future.save()

        # Event - register - online and free
        event_2_register_online_free_future = Event.objects.create(
            name='Introduction to Teaching CS with Zoom',
            description=(
                'TODO'
                'TODO'
            ),
            start=datetime.datetime(2023, 6, 1, 8, 0, 0),
            end=datetime.datetime(2023, 6, 1, 10, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            registration_type = 2,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
        )
        event_2_register_online_free_future.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_2_register_online_free_future.save()

        # Event - register - in person and costs
        event_3_register_physical_costs_future = Event.objects.create(
            name="Python Introduction",
            description=(
                'TODO'
                'TODO'
            ),   
            registration_type = 1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True,
            featured=True,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
        )
        event_3_register_physical_costs_future.locations.set([sample_location_2])
        event_3_register_physical_costs_future.ticket_types.set([ticket_paid_event_staff, ticket_paid_facilitator, ticket_paid_teacher])
        event_3_register_physical_costs_future.save()

        # Event - invite only
        event_4_invite_physical_free_future = Event.objects.create(
            name="Teaching with AI 2023",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 4,
            start=datetime.datetime(2023, 4, 15),
            end=datetime.datetime(2023, 4, 15),
            accessible_online=False,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_4_invite_physical_free_future.locations.set([sample_location_3])
        event_4_invite_physical_free_future.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_4_invite_physical_free_future.save()

        # Event - external link
        event_5_external_online_free_future = Event.objects.create(
            name="Intro to Computer Graphics",
            description=(
                'TODO'
                'TODO'
            ), 
            registration_type = 3,
            start=datetime.date(2023, 8, 15),
            end=datetime.date(2023, 8, 15),
            accessible_online=True,
            published=True,
            featured=True,
            registration_link='www.google.com',
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
        )
        event_5_external_online_free_future.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_5_external_online_free_future.save()

        # Events - 3 in past
        event_6_apply_online_free_past = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 2,
            start=datetime.datetime(2022, 4, 15, 10, 0, 0),
            end=datetime.datetime(2022, 4, 15, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_6_apply_online_free_past.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_6_apply_online_free_past.save()

        event_7_apply_online_free_past = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 2,
            start=datetime.datetime(2022, 3, 2, 10, 0, 0),
            end=datetime.datetime(2022, 3, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_7_apply_online_free_past.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_7_apply_online_free_past.save()

        event_8_register_online_free_future = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 1,
            start=datetime.datetime(2022, 1, 2, 10, 0, 0),
            end=datetime.datetime(2022, 1, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_8_register_online_free_future.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_8_register_online_free_future.save()

        # Events - 1 cancelled in past
        event_9_apply_online_free_past_cancelled = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 2,
            start=datetime.datetime(2022, 1, 2, 10, 0, 0),
            end=datetime.datetime(2022, 1, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_cancelled=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_9_apply_online_free_past_cancelled.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_9_apply_online_free_past_cancelled.save()

        # Events - 1 cancellevent_9_apply_online_free_past_cancelleded in future
        event_10_apply_online_free_past_cancelled = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 2,
            start=datetime.datetime(2023, 1, 2, 10, 0, 0),
            end=datetime.datetime(2023, 1, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_cancelled=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_10_apply_online_free_past_cancelled.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_10_apply_online_free_past_cancelled.save()

        # MORE EVENTS FOR USER STUDY PARTICIPANT TO HAVE APPLIED FOR
        # Addtional events for user study participant to see on their event applications page
        event_11_register_online_free_future_cancelled = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 1,
            start=datetime.datetime(2023, 1, 2, 10, 0, 0),
            end=datetime.datetime(2023, 1, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_cancelled=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_11_register_online_free_future_cancelled.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_11_register_online_free_future_cancelled.save()

        event_12_register_online_free_future = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 1,
            start=datetime.datetime(2023, 1, 2, 10, 0, 0),
            end=datetime.datetime(2023, 1, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_12_register_online_free_future.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_12_register_online_free_future.save()

        event_13_register_online_free_future = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 1,
            start=datetime.datetime(2023, 1, 2, 10, 0, 0),
            end=datetime.datetime(2023, 1, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_13_register_online_free_future.ticket_types.set([ticket_free_event_staff, ticket_free_facilitator, ticket_free_teacher])
        event_13_register_online_free_future.save()

        event_14_register_physical_costs_future = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 1,
            start=datetime.datetime(2023, 1, 2, 10, 0, 0),
            end=datetime.datetime(2023, 1, 2, 14, 0, 0),
            accessible_online=False,
            published=True,
            featured=True,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_14_register_physical_costs_future.locations.set([sample_location_1])
        event_14_register_physical_costs_future.ticket_types.set([ticket_paid_event_staff, ticket_paid_facilitator, ticket_paid_student, ticket_paid_teacher])
        event_14_register_physical_costs_future.save()

        event_15_register_physical_costs_past = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 1,
            start=datetime.datetime(2021, 1, 2, 10, 0, 0),
            end=datetime.datetime(2021, 1, 2, 14, 0, 0),
            accessible_online=False,
            published=True,
            featured=True,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_15_register_physical_costs_past.locations.set([sample_location_1])
        event_15_register_physical_costs_past.ticket_types.set([ticket_paid_event_staff, ticket_paid_facilitator, ticket_paid_student, ticket_paid_teacher])
        event_15_register_physical_costs_past.save()

        # Event - not published - use to step through each event phase as event staff
        event_16_register_physical_costs_future = Event.objects.create(
            name="TODO",
            description=(
                'TODO'
                'TODO'
            ),
            registration_type = 1,
            start=datetime.datetime(2021, 1, 2, 10, 0, 0),
            end=datetime.datetime(2021, 1, 2, 14, 0, 0),
            accessible_online=False,
            published=False,
            featured=True,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            )
        event_16_register_physical_costs_future.locations.set([sample_location_2])
        event_16_register_physical_costs_future.ticket_types.set([ticket_paid_event_staff, ticket_paid_facilitator, ticket_paid_student, ticket_paid_teacher])
        event_16_register_physical_costs_future.save()


        # EVENT IS STAFFED BY STUDY PARTICIPANT
        # Event applications - 10 for apply event
        event_application_apply_1 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_1,
            representing = "Myself",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_2 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_2,
            representing = "University of Canterbury",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_3 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_3,
            representing = "DTTA",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_4 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_4,
            representing = "My school",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_5 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_5,
            representing = "My school",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_6 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_6,
            representing = "My school",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_7 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_7,
            representing = "My school",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_8 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_8,
            representing = "My school",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_9 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_9,
            representing = "My school",
            event = event_1_apply_online_free_future,
        )

        event_application_apply_10 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_10,
            representing = "My school",
            event = event_1_apply_online_free_future,
        )

        # EVENT IS STAFFED BY STUDY PARTICIPANT
        # Event applications - 10 for register event (online and free) - mixture of 5 pending, 1 approved, 1 rejected, 3 withdraw (2 set reasons, 1 other reason)
        
        PENDING = 1
        APPROVED = 2
        REJECTED = 3
        
        event_application_register_1_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_1,
            representing = "Myself",
            event = event_2_register_online_free_future,
        )

        event_application_register_2_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_2,
            representing = "University of Canterbury",
            event = event_2_register_online_free_future,
        )

        event_application_register_3_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_3,
            representing = "DTTA",
            event = event_2_register_online_free_future,
        )

        event_application_register_4_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_4,
            representing = "My school",
            event = event_2_register_online_free_future,
        )

        event_application_register_5_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_5,
            representing = "My school",
            event = event_2_register_online_free_future,
        )

        event_application_register_6_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_6,
            representing = "My school",
            event = event_2_register_online_free_future,
            status = APPROVED
        )

        event_application_register_7_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_7,
            representing = "My school",
            event = event_2_register_online_free_future,
            status = APPROVED
        )

        event_application_register_8_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_8,
            representing = "My school",
            event = event_2_register_online_free_future,
            status = APPROVED
        )

        event_application_register_9_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_9,
            representing = "My school",
            event = event_2_register_online_free_future,
            status = REJECTED
        )

        event_application_register_10_online_free = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_10,
            representing = "My school",
            event = event_2_register_online_free_future,
            status = REJECTED
        )

        PREFER_NOT_TO_SAY = 1
        ILLNESS = 2
        NOT_INTERESTED = 3
        CHANGE_OF_PLANS = 4
        TOO_EXPENSIVE = 5
        INCONVENIENT_LOCATION = 6
        OTHER = 7

        event_application_register_online_free_withdrawn_1 = DeletedEventApplication.objects.create(
            deletion_reason = PREFER_NOT_TO_SAY,
            event = event_2_register_online_free_future
        )

        event_application_register_online_free__withdrawn_2 = DeletedEventApplication.objects.create(
            deletion_reason = NOT_INTERESTED,
            event = event_2_register_online_free_future
        )

        event_application_register_online_free_withdrawn_3 = DeletedEventApplication.objects.create(
            deletion_reason = TOO_EXPENSIVE,
            event = event_2_register_online_free_future
        )

        event_application_register_online_free_withdrawn_4 = DeletedEventApplication.objects.create(
            deletion_reason = OTHER,
            event = event_2_register_online_free_future,
            other_reason_for_deletion = "Clashes with another event I would like to attend."
        )

        event_application_register_online_free_withdrawn_4 = DeletedEventApplication.objects.create(
            deletion_reason = OTHER,
            event = event_2_register_online_free_future,
            other_reason_for_deletion = "Didn't realise the event was online."
        )
        
        # EVENT IS STAFFED BY STUDY PARTICIPANT
        # Event applications - 10 for register event (in person and costs and catered) - mixture of 5 pending, 1 approved, 1 rejected, 3 withdraw (2 set reasons, 1 other reason)

        event_application_register_1_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_event_staff,
            user = user_1,
            representing = "Myself",
            event = event_3_register_physical_costs_future,
            emergency_contact_first_name = "Daniel",
            emergency_contact_last_name = "Prince",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 21 126 0764"
        )

        event_application_register_2_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_teacher,
            user = user_2,
            representing = "University of Canterbury",
            event = event_3_register_physical_costs_future,
            emergency_contact_first_name = "Neha",
            emergency_contact_last_name = "Richardson",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 29 370 1241"
        )

        event_application_register_3_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_free_facilitator,
            user = user_3,
            representing = "DTTA",
            event = event_3_register_physical_costs_future,
            emergency_contact_first_name = "Lilian",
            emergency_contact_last_name = "Field",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 21 805 437"
        )

        event_application_register_4_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_event_staff,
            user = user_4,
            representing = "My school",
            event = event_3_register_physical_costs_future,
            emergency_contact_first_name = "Leonardo",
            emergency_contact_last_name = "Sparrow",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 22 1382 0407"
        )

        event_application_register_5_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_student,
            user = user_5,
            representing = "My school",
            event = event_3_register_physical_costs_future,
            emergency_contact_first_name = "Stefano",
            emergency_contact_last_name = "Peralta",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 20 9484 4821"
        )

        event_application_register_6_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_teacher,
            user = user_6,
            representing = "My school",
            event = event_3_register_physical_costs_future,
            status = APPROVED,
            emergency_contact_first_name = "Amelia",
            emergency_contact_last_name = "Short",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 21 514 286"
        )

        event_application_register_7_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_teacher,
            user = user_7,
            representing = "My school",
            event = event_3_register_physical_costs_future,
            status = APPROVED,
            emergency_contact_first_name = "Aleisha",
            emergency_contact_last_name = "Galvan",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 20 617 6478"
        )

        event_application_register_8_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_teacher,
            user = user_8,
            representing = "My school",
            event = event_3_register_physical_costs_future,
            status = APPROVED,
            emergency_contact_first_name = "Jasmin",
            emergency_contact_last_name = "Rayner",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 22 614 5719"
        )

        event_application_register_9_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_teacher,
            user = user_9,
            representing = "My school",
            event = event_3_register_physical_costs_future,
            status = REJECTED,
            emergency_contact_first_name = "Maryam",
            emergency_contact_last_name = "Jensen",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 21 485 802"
        )

        event_application_register_10_physical_and_costs = EventApplication.objects.create(
            participant_type = ticket_paid_teacher,
            user = user_10,
            representing = "My school",
            event = event_3_register_physical_costs_future,
            status = REJECTED,
            emergency_contact_first_name = "Maison",
            emergency_contact_last_name = "Fernandez",
            emergency_contact_relationship = "Partner",
            emergency_contact_phone_number =  "+64 27 827 89384"
        )

        event_application_apply_withdrawn_1 = DeletedEventApplication.objects.create(
            deletion_reason = PREFER_NOT_TO_SAY,
            event = event_3_register_physical_costs_future
        )

        event_application_apply_withdrawn_2 = DeletedEventApplication.objects.create(
            deletion_reason = NOT_INTERESTED,
            event = event_3_register_physical_costs_future
        )

        event_application_apply_withdrawn_3 = DeletedEventApplication.objects.create(
            deletion_reason = TOO_EXPENSIVE,
            event = event_3_register_physical_costs_future
        )

        event_application_apply_withdrawn_4 = DeletedEventApplication.objects.create(
            deletion_reason = OTHER,
            event = event_3_register_physical_costs_future,
            other_reason_for_deletion = "Clashes with another event I would like to attend."
        )

        event_application_apply_withdrawn_4 = DeletedEventApplication.objects.create(
            deletion_reason = OTHER,
            event = event_3_register_physical_costs_future,
            other_reason_for_deletion = "Didn't realise the event was online."
        )

        # Add admin account to all events
        events = Event.objects.all()
        for event in events:
            event.event_staff.add(admin)
            event.save()
        admin.save()
        print('Admin account set as event staff for all events')

        # ADD EVENT STAFF TO THESE THREE EVENTS THAT HAVE EVENT APPLICATION
        event_1_apply_online_free_future.event_staff.add(user_study_participant)
        event_1_apply_online_free_future.save()
        event_2_register_online_free_future.event_staff.add(user_study_participant)
        event_2_register_online_free_future.save()
        event_3_register_physical_costs_future.event_staff.add(user_study_participant)
        event_3_register_physical_costs_future.save()
        user_study_participant.save()
        print('User study participant set as event staff for three events')

        # STUDY PARTICPANT'S 
        # 4 event applications - so 4 different non-staff events
        # 1) 3 that are free and online and in future - so can withdraw 2 (diff pages) and can update one
        study_user_event_application_1 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_study_participant,
            representing = "My school",
            event = event_8_register_online_free_future,
            status = APPROVED
        )
        study_user_event_application_2 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_study_participant,
            representing = "My school",
            event = event_12_register_online_free_future,
            status = APPROVED
        )
        study_user_event_application_3 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_study_participant,
            representing = "My school",
            event = event_13_register_online_free_future,
            status = APPROVED
        )

        # 2) 1 that costs and is in person and in future - so can update this (MAKE SURE DOESN'T GET WITHDRAWN!)
        study_user_event_application_4 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_study_participant,
            representing = "My school",
            event = event_14_register_physical_costs_future,
            status = APPROVED
        ) 

        # 3) 2 that are in past (one cancelled)
        study_user_event_application_5 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_study_participant,
            representing = "My school",
            event = event_9_apply_online_free_past_cancelled,
            status = APPROVED
        )
        study_user_event_application_6 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_study_participant,
            representing = "My school",
            event = event_6_apply_online_free_past,
            status = APPROVED
        )

        # 4) 1 that is reject and in the past
        study_user_event_application_7 = EventApplication.objects.create(
            participant_type = ticket_free_event_staff,
            user = user_study_participant,
            representing = "My school",
            event = event_15_register_physical_costs_past,
            status = REJECTED
        )


        # -------------------------- Realistic events for informal demonstrations --------------------------
        # TODO: finish creating realistic events

        # sample_location_1 = Location.objects.create(
        #   name='University of Canterbury',
        #   suburb='Ilam',
        #   city='Christchurch',
        #   region='14',
        #   coords=Point(-43, 172)
        # )
        # sample_location_2 = Location.objects.create(
        #     room='Room 456',
        #     name='Middleton Grange School',
        #     street_address='12 High Street',
        #     suburb='Riccarton',
        #     city='Chrirstchurch',
        #     region=14,
        #     coords=Point(-12, 149)
        # )

        # sample_location_3 = Location.objects.create(
        #     room='Room 7',
        #     name='Middleton Grange School',
        #     street_address='12 High Street',
        #     suburb='Riccarton',
        #     city='Chrirstchurch',
        #     region=14,
        #     coords=Point(-27, 188)
        # )

        # sample_location_1.save()
        # sample_location_2.save()
        # sample_location_3.save()

        # sample_event_free_1 = Event.objects.create(
        #     name='DTHM for Kaiako Conference 2021',
        #     description=(
        #         'Inspirational collaboration to build your confidence teaching DT & HM.\n\n'
        #         'This is a FREE face to face Digital Technologies Teachers Aotearoa (DTTA) subject '
        #         'association event, for all teachers in Aotearoa. It\'s all about building your '
        #         'practice as a kaiako, for your learners.\n\n'
        #         'Join us for 3 days of:\n\n'
        #         'Connecting and reconnecting with colleagues across Aotearoa\n\n'
        #         'Engaging with a team to uncover and bring to light inspirational learning resources\n\n'
        #         'Developing programmes of learning that you will confidently take '
        #         'into your classroom and use immediately',
        #     ),
        #     start=datetime.datetime(2023, 4, 23, 8, 0, 0),
        #     end=datetime.datetime(2023, 4, 23, 8, 0, 0),
        #     published=True,
        #     featured=True,
        #     price=0,
        # )

        # event_physical_register_1 = Event.objects.create(
        #     name="Python Introduction",
        #     description="Some description",
        #     registration_type = 1,
        #     start=datetime.date(2023, 6, 24),
        #     end=datetime.date(2023, 6, 26),
        #     accessible_online=False,
        #     price=50,
        #     published=True,
        #     featured=True,
        # )
        # # event_physical_register_1.locations.set(sample_location_2)
        # event_physical_register_1.save()

        # event_physical_apply_1 = Event.objects.create(
        #         name="Security in CS",
        #         description="Some description",
        #         registration_type = 2,
        #         start=datetime.date(2023, 2, 13),
        #         end=datetime.date(2023, 2, 14),
        #         accessible_online=False,
        #         price=75,
        #         published=True,
        #         featured=True,
        #     )
        # # event_physical_apply_1.locations.set(sample_location_2)
        # event_physical_apply_1.save()

        # event_physical_invite_1 = Event.objects.create(
        #         name="Teaching with AI 2023",
        #         description="Some description",
        #         registration_type = 4,
        #         start=datetime.date(2023, 4, 15),
        #         end=datetime.date(2023, 4, 15),
        #         accessible_online=False,
        #         price=0,
        #         published=True,
        #         featured=True,
        #     )
        # # event_physical_invite_1.locations.set(sample_location_3)
        # event_physical_invite_1.save()

        # event_physical_url_1 = Event.objects.create(
        #         name="Intro to Computer Graphics",
        #         description="Some description",
        #         registration_type = 3,
        #         start=datetime.date(2023, 8, 15),
        #         end=datetime.date(2023, 8, 15),
        #         accessible_online=False,
        #         price=0,
        #         published=True,
        #         featured=True,
        #         registration_link='www.google.com'
        #     )
        # # event_physical_url_1.locations.set(sample_location_3)
        # event_physical_url_1.save()

        # event_ended_1 = Event.objects.create(
        #         name="Teaching with AI 2021",
        #         description="Some description",
        #         registration_type = 4,
        #         start=datetime.date(2020, 4, 15),
        #         end=datetime.date(2020, 4, 15),
        #         accessible_online=False,
        #         price=0,
        #         published=True,
        #         featured=True,
        #     )
        # # event_physical_url_1.locations.set(sample_location_3)
        # event_physical_url_1.save()

        # TODO: free and paid events

        # --------------------------------------------------------------------------------------------------

        # RANDOMLY GENERATED SAMPLE DATA FOR DEVELOPING

        # User = get_user_model()

        # # Create admin account
        # admin = User.objects.create_superuser(
        #     'admin',
        #     'admin@dthm4kaiako.ac.nz',
        #     password=settings.SAMPLE_DATA_ADMIN_PASSWORD,
        #     first_name='Admin',
        #     last_name='Account'
        # )
        # EmailAddress.objects.create(
        #     user=admin,
        #     email=admin.email,
        #     primary=True,
        #     verified=True
        # )
        # print('Admin created.')

        # # Create user account
        # user = User.objects.create_user(
        #     'user',
        #     'user@dthm4kaiako.ac.nz',
        #     password=settings.SAMPLE_DATA_USER_PASSWORD,
        #     first_name='Alex',
        #     last_name='Doe'
        # )
        # EmailAddress.objects.create(
        #     user=user,
        #     email=user.email,
        #     primary=True,
        #     verified=True
        # )
        # print('User created.')

        # # Create entities
        # EntityFactory.create_batch(size=10)
        # print('Entities created.')

        # # Resources
        # Language.objects.create(name='English', css_class='language-en')
        # Language.objects.create(name='Māori', css_class='language-mi')
        # print('Languages created.')

        # curriculum_learning_areas = {
        #     'English': 'english',
        #     'Arts': 'arts',
        #     'Health and physical education': 'health-pe',
        #     'Learning languages': 'languages',
        #     'Mathematics and statistics': 'mathematics',
        #     'Science': 'science',
        #     'Social sciences': 'social-sciences',
        #     'Technology': 'technology',
        # }
        # for area_name, area_css_class in curriculum_learning_areas.items():
        #     CurriculumLearningArea.objects.create(
        #         name=area_name,
        #         css_class=area_css_class,
        #     )
        # print('Curriculum learning areas created.')

        # ta_ct = TechnologicalArea.objects.create(
        #     name='Computational thinking',
        #     abbreviation='CT',
        #     css_class='ta-ct',
        # )
        # for i in range(1, 9):
        #     ProgressOutcome.objects.create(
        #         name='Computational thinking - Progress outcome {}'.format(i),
        #         abbreviation='CT PO{}'.format(i),
        #         technological_area=ta_ct,
        #         css_class='po-ct',
        #     )
        # ta_dddo = TechnologicalArea.objects.create(
        #     name='Designing and developing digital outcomes',
        #     abbreviation='DDDO',
        #     css_class='ta-dddo',
        # )
        # for i in range(1, 7):
        #     ProgressOutcome.objects.create(
        #         name='Designing and developing digital outcomes - Progress outcome {}'.format(i),
        #         abbreviation='DDDO PO{}'.format(i),
        #         technological_area=ta_dddo,
        #         css_class='po-dddo',
        #     )
        # print('Technological areas created.')
        # print('Progress outcomes created.')

        # NZQAStandardFactory.create_batch(size=20)
        # for i in range(0, 14):
        #     YearLevel.objects.create(
        #         level=i
        #     )
        # print('NZQA standards created.')

        # ResourceFactory.create_batch(size=20)
        # print('Resources created.')

        # # Events
        # event_series = {
        #     (
        #         'Computer Science for High Schools',
        #         'CS4HS',
        #     ),
        #     (
        #         'Computer Science for Primary Schools',
        #         'CS4PS',
        #     ),
        #     (
        #         'Computer Science for Professional Development',
        #         'CS4PD',
        #     ),
        #     (
        #         'Code Club for Teachers',
        #         'CC4T',
        #     ),
        # }
        # for (name, abbreviation) in event_series:
        #     Series.objects.create(
        #         name=name,
        #         abbreviation=abbreviation,
        #     )
        # print('Event series created.')

        region_codes = dict()
        region_suffix = ' region'
        for (code, name) in REGION_CHOICES:
            if name.endswith(region_suffix):
                name = name[:-len(region_suffix)]
            region_codes[name] = code
        with open('general/management/commands/sample-data/nz-schools.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in random.sample(list(reader), 100):
                if row['Longitude'] and row['Latitude'] and row['Region']:
                    Location.objects.create(
                        room='Room A',
                        name=row['Name'],
                        street_address=row['Street'],
                        suburb=row['Suburb'],
                        city=row['City'],
                        region=region_codes[row['Region']],
                        coords=Point(
                            float(row['Longitude']),
                            float(row['Latitude'])
                        ),
                    )
        print('Event locations created.')

        # EventFactory.create_batch(size=50)
        # print('Events created.')

        # # DTTA
        # NewsArticleFactory.create_batch(size=20)
        # print('DTTA news articles created.')
        # PageFactory.create_batch(size=5)
        # print('DTTA pages created.')
        # ProjectFactory.create_batch(size=5)
        # print('DTTA projects created.')
        # RelatedLinkFactory.create_batch(size=10)
        # print('DTTA related links created.')

        # # POET
        # management.call_command('load_poet_data')
        # POETFormResourceFactory.create_batch(size=20)
        # print('POET resources created.')
        # POETFormProgressOutcomeGroupFactory.create_batch(size=6)
        # print('POET progress outcome groups created.')
        # POETFormSubmissionFactory.create_batch(size=800)
        # print('POET submissions created.')

        # # Event staff
        # events = Event.objects.all()
        # for event in events:
        #     event.event_staff.add(admin)
        #     event.save()
        # admin.save()
        # print('Admin account set as event staff for all events')

        # # Create common participant types
        # staff_ticket = Ticket.objects.create(name="Event Staff", price=0.0)
        # staff_ticket.save()
        # teacher_ticket = Ticket.objects.create(name="Teacher", price=0.0)
        # teacher_ticket.save()
        # student_ticket = Ticket.objects.create(name="Student", price=0.0)
        # student_ticket.save()
        # facilitator_ticket = Ticket.objects.create(name="Facilitator", price=0.0)
        # facilitator_ticket.save()

        # # Tickets
        # for event in events:
        #     event.ticket_types.add(staff_ticket)
        #     event.save()
