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
# User_Models
from users.models import (
    DietaryRequirement,
    Entity,
    User
)
# Events
from events.models import (
    DeletedEventRegistration,
    EventRegistration,
    Location,
    RegistrationForm,
    Series,
    ParticipantType,
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
        # dietary_requirement_none=DietaryRequirement.objects.create(name="None")
        dietary_requirement_dairy_free = DietaryRequirement.objects.create(name="Dairy free")
        dietary_requirement_gluten_free = DietaryRequirement.objects.create(name="Gluten free")
        dietary_requirement_vegetarian = DietaryRequirement.objects.create(name="Vegetarian")
        dietary_requirement_vegan = DietaryRequirement.objects.create(name="Vegan")
        dietary_requirement_dairy_free = DietaryRequirement.objects.create(name="FODMAP")
        dietary_requirement_halal = DietaryRequirement.objects.create(name="Halal")
        dietary_requirement_coffee = DietaryRequirement.objects.create(name="Give me coffee and no-one gets hurt")
        print('Dietary requirements created.')

        # Create standard participant type types
        participant_type_free_event_staff = ParticipantType.objects.create(name="Event Staff", price=0.0)
        participant_type_free_teacher = ParticipantType.objects.create(name="Teacher", price=0.0)
        participant_type_free_facilitator = ParticipantType.objects.create(name="Facilitator", price=0.0)
        participant_type_paid_event_staff = ParticipantType.objects.create(name="Event Staff", price=3.0)
        participant_type_paid_teacher = ParticipantType.objects.create(name="Teacher", price=50.0)
        participant_type_paid_student = ParticipantType.objects.create(name="Student", price=20.0)
        participant_type_paid_facilitator = ParticipantType.objects.create(name="Facilitator", price=25.0)
        print('Common participant types created.')

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

        User_Model = get_user_model()

        # Create admin account
        admin = User_Model.objects.create_superuser(
            'admin',
            'admin@dthm4kaiako.ac.nz',
            password=settings.SAMPLE_DATA_ADMIN_PASSWORD,
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

        # Create user account
        user = User_Model.objects.create_user(
            'user',
            'user@dthm4kaiako.ac.nz',
            password=settings.SAMPLE_DATA_USER_PASSWORD,
            first_name='Alex',
            last_name='Doe'
        )
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True
        )
        print('User_Model created.')

        # Create entities
        EntityFactory.create_batch(size=10)
        print('Entities created.')

        # Resources
        Language.objects.create(name='English', css_class='language-en')
        Language.objects.create(name='Māori', css_class='language-mi')
        print('Languages created.')

        curriculum_learning_areas = {
            'English': 'english',
            'Arts': 'arts',
            'Health and physical education': 'health-pe',
            'Learning languages': 'languages',
            'Mathematics and statistics': 'mathematics',
            'Science': 'science',
            'Social sciences': 'social-sciences',
            'Technology': 'technology',
        }
        for area_name, area_css_class in curriculum_learning_areas.items():
            CurriculumLearningArea.objects.create(
                name=area_name,
                css_class=area_css_class,
            )
        print('Curriculum learning areas created.')

        ta_ct = TechnologicalArea.objects.create(
            name='Computational thinking',
            abbreviation='CT',
            css_class='ta-ct',
        )
        for i in range(1, 9):
            ProgressOutcome.objects.create(
                name='Computational thinking - Progress outcome {}'.format(i),
                abbreviation='CT PO{}'.format(i),
                technological_area=ta_ct,
                css_class='po-ct',
            )
        ta_dddo = TechnologicalArea.objects.create(
            name='Designing and developing digital outcomes',
            abbreviation='DDDO',
            css_class='ta-dddo',
        )
        for i in range(1, 7):
            ProgressOutcome.objects.create(
                name='Designing and developing digital outcomes - Progress outcome {}'.format(i),
                abbreviation='DDDO PO{}'.format(i),
                technological_area=ta_dddo,
                css_class='po-dddo',
            )
        print('Technological areas created.')
        print('Progress outcomes created.')

        NZQAStandardFactory.create_batch(size=20)
        for i in range(0, 14):
            YearLevel.objects.create(
                level=i
            )
        print('NZQA standards created.')

        ResourceFactory.create_batch(size=20)
        print('Resources created.')

        # Events
        event_series = {
            (
                'Computer Science for High Schools',
                'CS4HS',
            ),
            (
                'Computer Science for Primary Schools',
                'CS4PS',
            ),
            (
                'Computer Science for Professional Development',
                'CS4PD',
            ),
            (
                'Code Club for Teachers',
                'CC4T',
            ),
        }
        for (name, abbreviation) in event_series:
            Series.objects.create(
                name=name,
                abbreviation=abbreviation,
            )
        print('Event series created.')

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

        EventFactory.create_batch(size=50)
        print('Events created.')

        # DTTA
        NewsArticleFactory.create_batch(size=20)
        print('DTTA news articles created.')
        PageFactory.create_batch(size=5)
        print('DTTA pages created.')
        ProjectFactory.create_batch(size=5)
        print('DTTA projects created.')
        RelatedLinkFactory.create_batch(size=10)
        print('DTTA related links created.')

        # POET
        management.call_command('load_poet_data')
        POETFormResourceFactory.create_batch(size=20)
        print('POET resources created.')
        POETFormProgressOutcomeGroupFactory.create_batch(size=6)
        print('POET progress outcome groups created.')
        POETFormSubmissionFactory.create_batch(size=800)
        print('POET submissions created.')

        # Event staff
        events = Event.objects.all()
        for event in events:
            event.event_staff.add(admin)
            event.save()
        admin.save()
        print('Admin account set as event staff for all events')

        # Participants
        for event in events:
            event.participant_types.add(participant_type_free_event_staff)
            event.save()


# ------------------- SAMPLE DATA FOR USER STUDY -------------------------

        # Create user accounts
        user_1 = User_Model()
        user_1 = User_Model.objects.create_user(
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

        print('User_Model 1 created.')

        user_2 = User_Model()
        user_2 = User_Model.objects.create_user(
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
        print('User_Model 2 created.')

        user_3 = User_Model()
        user_3 = User_Model.objects.create_user(
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
        print('User_Model 3 created.')

        user_4 = User_Model()
        user_4 = User_Model.objects.create_user(
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
        print('User_Model 4 created.')

        user_5 = User_Model()
        user_5 = User_Model.objects.create_user(
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
        print('User_Model 5 created.')

        user_6 = User_Model()
        user_6 = User_Model.objects.create_user(
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
        user_6.dietary_requirements.set([dietary_requirement_halal])
        user_6.educational_entities.set([entity_6])
        user_6.save()
        print('User_Model 6 created.')

        user_7 = User_Model()
        user_7 = User_Model.objects.create_user(
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
        user_7.dietary_requirements.set([dietary_requirement_dairy_free])
        user_7.educational_entities.set([entity_7])
        user_7.save()
        print('User_Model 7 created.')

        user_8 = User_Model()
        user_8 = User_Model.objects.create_user(
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
        user_8.dietary_requirements.set([dietary_requirement_gluten_free])
        user_8.educational_entities.set([entity_8])
        user_8.save()
        print('User_Model 8 created.')

        user_9 = User_Model()
        user_9 = User_Model.objects.create_user(
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
        user_9.dietary_requirements.set([dietary_requirement_dairy_free])
        user_9.educational_entities.set([entity_9])
        user_9.save()
        print('User_Model 9 created.')

        user_10 = User_Model()
        user_10 = User_Model.objects.create_user(
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
        print('User_Model 10 created.')

        user_11 = User_Model()
        user_11 = User_Model.objects.create_user(
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
        print('User_Model 11 created.')

        user_12 = User_Model()
        user_12 = User_Model.objects.create_user(
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
        user_12.dietary_requirements.set([dietary_requirement_dairy_free])
        user_12.educational_entities.set([entity_12, entity_13, entity_14])
        user_12.save()
        print('User_Model 12 created.')

        demo_user = User_Model()
        demo_user = User_Model.objects.create_user(
            'user',
            'demo_user@dthm4kaiako.ac.nz',
            password="password",
            first_name='Hayley',
            last_name='Krippner',
            user_region=REGION_CANTERBURY,
            mobile_phone_number='+64 21 545 878'
        )
        EmailAddress.objects.create(
            user=demo_user,
            email=demo_user.email,
            primary=True,
            verified=True
        )
        print('User_Model 13 created - user study participant.')

        User.objects.filter(first_name="Hayley").update(email="demo@demo.co.nz")

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
            name='DTHM for Kaiako Conference 2023',
            description=(
                'Inspirational collaboration to build your confidence teaching DT & HM.\n\n'
                'This is a FREE face to face Digital Technologies Teachers Aotearoa (DTTA) subject '
                'association event, for all teachers in Aotearoa. It\'s all about building your '
                'practice as a kaiako, for your learners.\n\n'
                'Join us for 3 days of:\n\n'
                'Connecting and reconnecting with colleagues across Aotearoa\n\n'
                'Engaging with a team to uncover and bring to light inspirational learning resources\n\n'
                'Developing programmes of learning that you will confidently take '
                'into your classroom and use immediately'
            ),
            start=datetime.datetime(2023, 4, 23, 8, 0, 0),
            end=datetime.datetime(2023, 4, 23, 11, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            registration_type=2,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
        )
        event_1_apply_online_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_1_apply_online_free_future.save()

        # Event - register - online and free
        event_2_register_online_free_future = Event.objects.create(
            name='Practical ideas to teach the new digital technologies content',
            description=(
                'Join the UC CSERG (Department of Fun Stuff) team to learn how to'
                ' teach computational thinking and programming through practical '
                'activities that you can take back to your tamariki and use immediately.'
                ' This workshop is free and includes coffee in the morning as well as lunch.'
            ),
            start=datetime.datetime(2023, 6, 1, 8, 0, 0),
            end=datetime.datetime(2023, 6, 1, 10, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            registration_type=2,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
        )
        event_2_register_online_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_2_register_online_free_future.save()

        # Event - register - in person and costs
        event_3_register_physical_costs_future = Event.objects.create(
            name="Code Club 4 Teachers Digital Storytelling (face to face)",
            description=(
                'Whether you are an absolute beginner or someone who has dabbled with '
                'programming and coding. Our focus is on having fun while integrating '
                'Digital Technologies into your classroom programme.\n\n'
                'Join Amy Souquet and explore how to integrate digital technologies '
                'and computational thinking into curriculum areas and gain an understanding '
                'of the fundamentals of programming using age appropriate programming languages.'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True,
            featured=False,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
        )
        event_3_register_physical_costs_future.locations.set([sample_location_2])
        event_3_register_physical_costs_future.participant_types.set(
            [
                participant_type_paid_event_staff,
                participant_type_paid_facilitator,
                participant_type_paid_teacher
            ]
        )
        event_3_register_physical_costs_future.save()

        # Event - invite only
        event_4_invite_physical_free_future = Event.objects.create(
            name="Encryption, cryptosystems and ciphers",
            description=(
                'This three part series focuses on these cool concepts that'
                ' keep us safe online.'
                'Join Tim Bell and Tracy Henderson to explore why it\'s '
                'important to know what\'s'
                ' happening with your password and why you should have '
                'warning bells if a company emails you back your password.\n\n'
            ),
            registration_type=4,
            start=datetime.datetime(2023, 4, 15),
            end=datetime.datetime(2023, 4, 15),
            accessible_online=False,
            published=True,
            featured=False,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_4_invite_physical_free_future.locations.set([sample_location_3])
        event_4_invite_physical_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_4_invite_physical_free_future.save()

        # Event - external link
        event_5_external_online_free_future = Event.objects.create(
            name="Inspire your learners through creating great ideas through Digital Technologies",
            description=(
                'Use the UN sustainable development goals to generate great ideas for real world Digital'
                ' Technologies projects (Not yet started, Now underway, 2020 ready, Leading and innovating).\n\n'
                'Real-world projects will interest and motivate your learners - as well as provide scope for '
                'incorporating a range of NZC learning areas. In this 30 minute virtual session you will use '
                'the UN sustainable development goals to generate a range of great ideas for DT projects and '
                'share them with your fellow participants.\n\n'
                'This virtual meetup is aligned to the Ministry of Education’s digital technologies '
                'implementation support tool and starts at being 2020 ready as it supports you to continue to '
                'get into the detail of the curriculum content and grow your own understanding and leading and '
                'innovating by supporting you to feel confident with an Ako style of teaching and learning.'
            ),
            registration_type=3,
            start=datetime.date(2023, 8, 15),
            end=datetime.date(2023, 8, 15),
            accessible_online=True,
            published=True,
            featured=False,
            external_event_registration_link='www.google.com',
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
        )
        event_5_external_online_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_5_external_online_free_future.save()

        # Events - 3 in past
        event_6_apply_online_free_past = Event.objects.create(
            name="Solving Problems by Design",
            description=(
                'Technology is intervention by design. '
                'How do you get your ākonga using a good design process? What '
                'is the design process anyway?\n\n'
                'Explore the relationship between design and digital technology '
                'with this discussion-based hui. '
                'This session is an overview of how a design process can be '
                'used with your students. '
                'For a more comprehensive breakdown, including discussion, we '
                'highly recommend also attending '
                'the \'A Design Process\' sessions on Tuesday the 15th and 22nd '
                'of September.\n\n'
                'This virtual meetup is aligned to the Ministry of Education\'s '
                'digital technologies implementation '
                'support tool and starts at \'now underway\'. It supports you to '
                'unpack the detail, get organised for change, '
                'through being \'2020 ready\', to \'leading and innovating\', by'
                ' supporting you to feel confident with an '
                'Ako style of teaching and learning.'
            ),
            registration_type=2,
            start=datetime.datetime(2022, 4, 15, 10, 0, 0),
            end=datetime.datetime(2022, 4, 15, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_6_apply_online_free_past.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_6_apply_online_free_past.save()

        event_7_apply_online_free_past = Event.objects.create(
            name="How to make informed decisions when buying DT resources",
            description=(
                'There are a lot of DT resources and activities available, so how do you evaluate them?'
                ' Trevor and Melissa will work through things to consider when looking at resources '
                'that will interest and challenge your learners.\n\n'
                'Digital Technologies learning should now be part of your curriculum. We are here to '
                'support you to achieve this. As you plan and implement the new digital technologies '
                'curriculum content you will need to evaluate and select learning resources that '
                'will interest and challenge your learners. This 30 minute session will get you '
                'thinking about what makes for a great resource - as well as seeking advice and '
                'sharing successes with colleagues.\n\n'
                'This virtual meetup is aligned to the Ministry of Education’s digital technologies '
                'implementation support tool and starts at \'now underway\'. It supports you to unpack '
                'the detail, get organised for change, through being \'2020 ready\', to \'leading and '
                'innovating\', by supporting you to feel confident with an Ako style of teaching and learning.'
            ),
            registration_type=2,
            start=datetime.datetime(2022, 3, 2, 10, 0, 0),
            end=datetime.datetime(2022, 3, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_7_apply_online_free_past.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_7_apply_online_free_past.save()

        event_8_register_online_free_future = Event.objects.create(
            name="Code Club 4 Teachers Sustainability",
            description=(
                'Mondays 3.30pm to 5.00pm. Whether you are an absolute beginner or '
                'someone who has dabbled with programming and coding. Our focus is '
                'on having fun while integrating Digital Technologies into your '
                'classroom programme.\n\n'
                'Join Kate Allan and explore how to integrate digital technologies and '
                'computational thinking into curriculum areas and gain an understanding '
                'of the fundamentals of programming using age appropriate programming languages.'
            ),
            registration_type=1,
            start=datetime.datetime(2022, 1, 2, 10, 0, 0),
            end=datetime.datetime(2022, 1, 2, 14, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_8_register_online_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_8_register_online_free_future.save()

        # Events - 1 cancelled in past
        event_9_apply_online_free_past_cancelled = Event.objects.create(
            name="Introduction to 3D Design Tinkercad",
            description=(
                'A three part introduction series to 3D design by using basic '
                'shapes to create more advanced objects.\n\n'
                'These three webinars will be looking at using Tinkercad and how'
                ' we can use it to build 3D objects from a blank canvas. Tinkercad '
                'is easy to understand which makes getting it onto the classroom hassle free.\n\n'
                'The first webinar will be introducing Tinkercad, the second and third webinars '
                'will be using 3D shapes to explore possibilities. We will also look at how these '
                'activities relate to progress outcomes and the Technology learning area. Note: '
                'these sessions will be interactive with participants being guided to use Tinkercad '
                'themselves throughout the sessions. No prior experience in Tinkercad is required.'
            ),
            registration_type=2,
            start=datetime.datetime(2022, 7, 7, 10, 0, 0),
            end=datetime.datetime(2022, 7, 7, 12, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            is_cancelled=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_9_apply_online_free_past_cancelled.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_9_apply_online_free_past_cancelled.save()

        # Events - 1 cancellevent_9_apply_online_free_past_cancelleded in future
        event_10_apply_online_free_past_cancelled = Event.objects.create(
            name="DT and Science - A Sound Investigation",
            description=(
                'Wondering how to integrate Computational thinking, and Designing and developing '
                'digital outcomes into your teaching of science for Years 5-10? Here are some ideas.'
                'This webinar will guide you through a comprehensive resource showing how an authentic '
                'context, such as teenage hearing loss due to loud music, can be used to integrate '
                'digital technologies opportunities into your classroom teaching. The webinar will '
                'be delivered in English, however, the content will be really beneficial to kura Māori '
                'also. We invite all Māori Medium kaiako to attend as the skills and knowledge covered '
                'in these sessions are relevant to Māori Medium contexts. This virtual meetup is aligned '
                'to the Ministry of Education’s digital technologies implementation support tool and starts '
                'at \'now underway\'. It supports you to unpack the detail, get organised for change, '
                'through being \'2020 ready\', to \'leading and innovating\', by supporting you to feel '
                'confident with an Ako style of teaching and learning.'
            ),
            registration_type=2,
            start=datetime.datetime(2023, 9, 13, 17, 0, 0),
            end=datetime.datetime(2023, 9, 13, 18, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            is_cancelled=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_10_apply_online_free_past_cancelled.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_10_apply_online_free_past_cancelled.save()

        # MORE EVENTS FOR USER STUDY PARTICIPANT TO HAVE APPLIED FOR
        # Addtional events for user study participant to see on their event registrations page
        event_11_register_online_free_future_cancelled = Event.objects.create(
            name="How binary digits rule the world",
            description=(
                'There is a hidden code that runs the world from food production to the '
                'air conditioning in your car. Learn to crack the code at this webinar.\n\n'
                'Everything computers do is based on binary digits. Everything controlled by computers, '
                'from digital clocks to airplanes, relies on binary digits. Find out how easy it is to '
                'have fun with this fundamental concept with your students and potentially prevent'
                ' future digital failures.\n\n'
                'Binary digits are first mentioned in progress outcome 3 but the activities shown '
                'in this webinar support younger students also.'
                'This virtual meetup is aligned to the Ministry of Education\'s digital technologies '
                'implementation support tool and starts at now underway as it supports you to unpack '
                'the detail and get organised for change and takes you through to being 2020 ready '
                'and leading and innovating by supporting you to feel confident with an '
                'Ako style of teaching and learning.'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 1, 19, 16, 0, 0),
            end=datetime.datetime(2023, 1, 19, 18, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            is_cancelled=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_11_register_online_free_future_cancelled.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_11_register_online_free_future_cancelled.save()

        event_12_register_online_free_future = Event.objects.create(
            name="Make great decisions - what should be on the purchasing plan?",
            description=(
                'Ask canny questions to ensure you make cost-effective Digital Technologies '
                'purchases (Not yet started, Now underway, 2020 ready, Leading and innovating)'
                'As you develop and trail programmes of learning, you are likely to consider '
                'buying digital devices and digital tools and gadgets. This 30 minute virtual '
                'session will help you ask canny questions, avoid hype and guide you in making '
                'purchases that provide great value for your time, effort and dollars as you '
                'implement the new Digital Technologies curriculum content. You will also have '
                'an opportunity to seek advice and share successes with colleagues.'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 4, 19, 13, 0, 0),
            end=datetime.datetime(2023, 4, 19, 17, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_12_register_online_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_12_register_online_free_future.save()

        event_13_register_online_free_future = Event.objects.create(
            name="DT Escape Room for the Curious",
            description=(
                'Digital Technologies escape room for the Curious. This event is a '
                'chance to explore the new and revised Digital Technologies curriculum '
                'content in a fun way. You’ll work together to solve challenges to escape '
                'from a (virtual) forest, with challenges inspired by the legends of Māui '
                'and what he would do to solve these problems.. You don’t need to be '
                'familiar with DT to do this, and you’ll pick up some ideas along the way, '
                'including ways to use the escape room approach in your own classroom to engage '
                'students. You can join the session alone and we’ll help you form a team, or '
                'you can bring your own group, either sharing one device or on their own devices.'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 10, 6, 7, 0, 0),
            end=datetime.datetime(2023, 10, 6, 9, 0, 0),
            accessible_online=True,
            published=True,
            featured=True,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_13_register_online_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_13_register_online_free_future.save()

        event_14_register_physical_costs_future = Event.objects.create(
            name="Facial recognition, what's it all about?",
            description=(
                'Thursday 3.30pm to 4.00pm. Have you been asked to "tag" '
                'in people on online platforms? '
                'Ever wondered how that works? Discover the algorithmic thinking '
                'that is happening behind the scenes.\n\n'
                'Join Tracy Henderson to explore the computer science '
                'behind facial recognition and '
                'how this impacts what we share online.\n\n'
                'This virtual meetup is aligned to the Ministry of Education\'s '
                'digital technologies implementation support tool and starts at \'now underway\'.'
                'It supports you to unpack the details, get organised for change, '
                'through being \'2020 ready\','
                ' to \'leading and innovating\', by supporting you to feel '
                'confident with an Ako style of teaching and learning.'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 8, 12, 10, 0, 0),
            end=datetime.datetime(2023, 8, 12, 16, 0, 0),
            accessible_online=False,
            published=True,
            featured=True,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_14_register_physical_costs_future.locations.set([sample_location_1])
        event_14_register_physical_costs_future.participant_types.set(
            [
                participant_type_paid_event_staff,
                participant_type_paid_facilitator,
                participant_type_paid_student,
                participant_type_paid_teacher
            ]
        )
        event_14_register_physical_costs_future.save()

        event_15_register_physical_costs_past = Event.objects.create(
            name="Design Thinking Process",
            description=(
                'Let\'s look at the design thinking process and '
                'how it can be incorporated into programmes.'
                'The design process is an approach to learning, collaboration, '
                'and problem solving within Digital Technologies. We will be '
                'looking at why and how we can be using this process to '
                'enhance and support students\' thinking and creativity.'
                'This virtual meetup is aligned to the Ministry of Education’s digital technologies '
                'implementation support tool and starts at being 2020 ready as it supports you to continue to '
                'get into the detail of the curriculum content and grow your own understanding and leading and '
                'innovating by supporting you to feel confident with an Ako style of teaching and learning.'
            ),
            registration_type=1,
            start=datetime.datetime(2021, 3, 9, 9, 0, 0),
            end=datetime.datetime(2021, 3, 29, 11, 0, 0),
            accessible_online=False,
            published=True,
            featured=True,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_15_register_physical_costs_past.locations.set([sample_location_1])
        event_15_register_physical_costs_past.participant_types.set(
            [
                participant_type_paid_event_staff,
                participant_type_paid_facilitator,
                participant_type_paid_student,
                participant_type_paid_teacher
            ]
        )
        event_15_register_physical_costs_past.save()

        # Event - not published - use to step through each event phase as event staff
        event_16_register_physical_costs_future = Event.objects.create(
            name="Programming with the Department of Fun Stuff",
            description=(
                'This three-day workshop is a gentle introduction to programming '
                '(sometimes referred to as the more mysterious sounding “coding”) '
                'for teachers with little or no prior experience. We\'ll start from '
                'absolute basics, and gently introduce the idea of what programming is, '
                'what it looks like, and help you develop some basic skills in either the '
                'Scratch or Python programming languages. We\'ll demystify the language of '
                'Computational Thinking, including ideas like “sequence”, “selection” and '
                '“iteration”, and explore what “debugging” looks like in a school context. '
                'The workshops will have breakout sessions for people who want to go at a '
                'faster or slower pace. And the main rule is that there are no silly '
                'questions - it\'s a chance to explore in a safe environment. We\'ll '
                'use examples that are relevant to our context in Aotearoa, and explore '
                'ideas that are relevant to the new and revised Digital '
                'Technologies curriculum content.\n\n'
                'The course will be run by Tim Bell, who has been teaching programming '
                'for way longer than he\'ll admit, but is particularly interested in '
                'first steps for beginners. He will be assisted by tutors from his '
                'CS Education Research group at Canterbury (also known '
                'as the department of fun stuff).\n'
                'This course is free, but we don\'t cover travel and accommodation, '
                'and you will need to make your own arrangements for this if you\'re '
                'coming from out of town. This is a great chance for you to support '
                'the local tourist industry! We won\'t start properly until 10am on '
                'Tuesday, and will finish by 3pm on Thursday, to allow for those who '
                'want to fly on those days - but if you have time to enjoy Christchurch, '
                'do take an extra day or two to explore the cafes and laneways '
                'of our vibrant rebuilt city!'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 1, 2, 10, 0, 0),
            end=datetime.datetime(2023, 1, 2, 14, 0, 0),
            accessible_online=False,
            published=False,
            featured=True,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
            )
        event_16_register_physical_costs_future.locations.set([sample_location_2])
        event_16_register_physical_costs_future.participant_types.set(
            [
                participant_type_paid_event_staff,
                participant_type_paid_facilitator,
                participant_type_paid_student,
                participant_type_paid_teacher
            ]
        )
        event_16_register_physical_costs_future.save()

        # EVENT IS STAFFED BY STUDY PARTICIPANT
        # Event registrations - 10 for apply event
        # event_registration_apply_1
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_1,
            representing="Myself",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_2
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_2,
            representing="University of Canterbury",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_3
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_3,
            representing="DTTA",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_4
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_4,
            representing="My school",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_5
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_5,
            representing="My school",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_6
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_6,
            representing="My school",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_7
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_7,
            representing="My school",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_8
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_8,
            representing="My school",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_9
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_9,
            representing="My school",
            event=event_1_apply_online_free_future,
        )

        # event_registration_apply_10
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_10,
            representing="My school",
            event=event_1_apply_online_free_future,
        )

        # EVENT IS STAFFED BY STUDY PARTICIPANT
        # Event registrations - 10 for register event (online and free)
        # --> mixture of 5 pending, 1 approved, 1 declined, 3 withdraw (2 set reasons, 1 other reason)

        # PENDING=1
        APPROVED = 2
        declined = 3

        # event_registration_register_1_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_1,
            representing="Myself",
            event=event_2_register_online_free_future,
        )

        # event_registration_register_2_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_2,
            representing="University of Canterbury",
            event=event_2_register_online_free_future,
        )

        # event_registration_register_3_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_3,
            representing="DTTA",
            event=event_2_register_online_free_future,
        )

        # event_registration_register_4_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_4,
            representing="My school",
            event=event_2_register_online_free_future,
        )

        # event_registration_register_5_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_5,
            representing="My school",
            event=event_2_register_online_free_future,
        )

        # event_registration_register_6_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_6,
            representing="My school",
            event=event_2_register_online_free_future,
            status=APPROVED
        )

        # event_registration_register_7_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_7,
            representing="My school",
            event=event_2_register_online_free_future,
            status=APPROVED
        )

        # event_registration_register_8_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_8,
            representing="My school",
            event=event_2_register_online_free_future,
            status=APPROVED
        )

        # event_registration_register_9_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_9,
            representing="My school",
            event=event_2_register_online_free_future,
            status=declined
        )

        # event_registration_register_10_online_free
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=user_10,
            representing="My school",
            event=event_2_register_online_free_future,
            status=declined
        )

        PREFER_NOT_TO_SAY = 1
        # ILLNESS=2
        NOT_INTERESTED = 3
        # CHANGE_OF_PLANS=4
        TOO_EXPENSIVE = 5
        # INCONVENIENT_LOCATION=6
        OTHER = 7

        # event_registration_register_online_free_withdrawn_1
        DeletedEventRegistration.objects.create(
            withdraw_reason=PREFER_NOT_TO_SAY,
            event=event_2_register_online_free_future
        )

        # event_registration_register_online_free__withdrawn_2
        DeletedEventRegistration.objects.create(
            withdraw_reason=NOT_INTERESTED,
            event=event_2_register_online_free_future
        )

        # event_registration_register_online_free_withdrawn_3
        DeletedEventRegistration.objects.create(
            withdraw_reason=TOO_EXPENSIVE,
            event=event_2_register_online_free_future
        )

        # event_registration_register_online_free_withdrawn_4
        DeletedEventRegistration.objects.create(
            withdraw_reason=OTHER,
            event=event_2_register_online_free_future,
            other_reason_for_withdrawing="Clashes with another event I would like to attend."
        )

        # event_registration_register_online_free_withdrawn_4
        DeletedEventRegistration.objects.create(
            withdraw_reason=OTHER,
            event=event_2_register_online_free_future,
            other_reason_for_withdrawing="Didn't realise the event was online."
        )

        # EVENT IS STAFFED BY STUDY PARTICIPANT
        # Event registrations - 10 for register event (in person and costs and catered)
        # --> mixture of 5 pending, 1 approved, 1 declined, 3 withdraw (2 set reasons, 1 other reason)

        # event_registration_register_1_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_event_staff,
            user=user_1,
            representing="Myself",
            event=event_3_register_physical_costs_future,
            emergency_contact_first_name="Daniel",
            emergency_contact_last_name="Prince",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 21 126 0764"
        )

        # event_registration_register_2_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_teacher,
            user=user_2,
            representing="University of Canterbury",
            event=event_3_register_physical_costs_future,
            emergency_contact_first_name="Neha",
            emergency_contact_last_name="Richardson",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 29 370 1241"
        )

        # event_registration_register_3_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_free_facilitator,
            user=user_3,
            representing="DTTA",
            event=event_3_register_physical_costs_future,
            emergency_contact_first_name="Lilian",
            emergency_contact_last_name="Field",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 21 805 437"
        )

        # event_registration_register_4_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_event_staff,
            user=user_4,
            representing="My school",
            event=event_3_register_physical_costs_future,
            emergency_contact_first_name="Leonardo",
            emergency_contact_last_name="Sparrow",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 22 1382 0407"
        )

        # event_registration_register_5_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_student,
            user=user_5,
            representing="My school",
            event=event_3_register_physical_costs_future,
            emergency_contact_first_name="Stefano",
            emergency_contact_last_name="Peralta",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 20 9484 4821"
        )

        # event_registration_register_6_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_teacher,
            user=user_6,
            representing="My school",
            event=event_3_register_physical_costs_future,
            status=APPROVED,
            emergency_contact_first_name="Amelia",
            emergency_contact_last_name="Short",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 21 514 286"
        )

        # event_registration_register_7_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_teacher,
            user=user_7,
            representing="My school",
            event=event_3_register_physical_costs_future,
            status=APPROVED,
            emergency_contact_first_name="Aleisha",
            emergency_contact_last_name="Galvan",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 20 617 6478"
        )

        # event_registration_register_8_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_teacher,
            user=user_8,
            representing="My school",
            event=event_3_register_physical_costs_future,
            status=APPROVED,
            emergency_contact_first_name="Jasmin",
            emergency_contact_last_name="Rayner",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 22 614 5719"
        )

        # event_registration_register_9_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_teacher,
            user=user_9,
            representing="My school",
            event=event_3_register_physical_costs_future,
            status=declined,
            emergency_contact_first_name="Maryam",
            emergency_contact_last_name="Jensen",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 21 485 802"
        )

        # event_registration_register_10_physical_and_costs
        EventRegistration.objects.create(
            participant_type=participant_type_paid_teacher,
            user=user_10,
            representing="My school",
            event=event_3_register_physical_costs_future,
            status=declined,
            emergency_contact_first_name="Maison",
            emergency_contact_last_name="Fernandez",
            emergency_contact_relationship="Partner",
            emergency_contact_phone_number="+64 27 827 89384"
        )

        # event_registration_apply_withdrawn_1
        DeletedEventRegistration.objects.create(
            withdraw_reason=PREFER_NOT_TO_SAY,
            event=event_3_register_physical_costs_future
        )

        # event_registration_apply_withdrawn_2
        DeletedEventRegistration.objects.create(
            withdraw_reason=NOT_INTERESTED,
            event=event_3_register_physical_costs_future
        )

        # event_registration_apply_withdrawn_3
        DeletedEventRegistration.objects.create(
            withdraw_reason=TOO_EXPENSIVE,
            event=event_3_register_physical_costs_future
        )

        # event_registration_apply_withdrawn_4
        DeletedEventRegistration.objects.create(
            withdraw_reason=OTHER,
            event=event_3_register_physical_costs_future,
            other_reason_for_withdrawing="Clashes with another event I would like to attend."
        )

        # event_registration_apply_withdrawn_4
        DeletedEventRegistration.objects.create(
            withdraw_reason=OTHER,
            event=event_3_register_physical_costs_future,
            other_reason_for_withdrawing="Didn't realise the event was online."
        )

        # Add admin account to all events
        events = Event.objects.all()
        for event in events:
            event.event_staff.add(admin)
            event.save()
        admin.save()
        print('Admin account set as event staff for all events')

        # ADD EVENT STAFF TO THESE THREE EVENTS THAT HAVE EVENT registration
        event_1_apply_online_free_future.event_staff.set([admin, demo_user])
        event_1_apply_online_free_future.save()
        event_2_register_online_free_future.event_staff.set([admin, demo_user])
        event_2_register_online_free_future.save()
        event_3_register_physical_costs_future.event_staff.set([admin, demo_user])
        event_3_register_physical_costs_future.save()
        event_16_register_physical_costs_future.event_staff.set([admin, demo_user])
        event_16_register_physical_costs_future.save()
        demo_user.save()
        print('User_Model study participant set as event staff for three events')

        event_1_reg_form_pk = event_1_apply_online_free_future.registration_form
        event_1_reg_form = RegistrationForm.objects.filter(pk=event_1_reg_form_pk)
        event_1_reg_form.update(
            open_datetime=datetime.datetime(2022, 1, 1, 0, 0, 0),
            close_datetime=datetime.datetime(2022, 4, 1, 0, 0, 0)
        )
        event_1_apply_online_free_future.save()

        event_2_reg_form_pk = event_2_register_online_free_future.registration_form
        event_2_reg_form = RegistrationForm.objects.filter(pk=event_2_reg_form_pk)
        event_2_reg_form.update(
            open_datetime=datetime.datetime(2022, 1, 1, 0, 0, 0),
            close_datetime=datetime.datetime(2022, 4, 1, 0, 0, 0)
        )
        event_2_register_online_free_future.save()

        event_3_reg_form_pk = event_3_register_physical_costs_future.registration_form
        event_3_reg_form = RegistrationForm.objects.filter(pk=event_3_reg_form_pk)
        event_3_reg_form.update(
            open_datetime=datetime.datetime(2022, 1, 1, 0, 0, 0),
            close_datetime=datetime.datetime(2022, 4, 1, 0, 0, 0)
        )
        event_3_register_physical_costs_future.save()

        # STUDY PARTICPANT'S
        # 4 event registrations - so 4 different non-staff events
        # 1) 3 that are free and online and in future - so can withdraw 2 (diff pages) and can update one
        # study_user_event_registration_1
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_8_register_online_free_future,
            status=APPROVED
        )
        # study_user_event_registration_2
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_12_register_online_free_future,
            status=APPROVED
        )
        # study_user_event_registration_3
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_13_register_online_free_future,
        )

        # 2) 1 that costs and is in person and in future - so can update this (MAKE SURE DOESN'T GET WITHDRAWN!)
        # study_user_event_registration_4
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_14_register_physical_costs_future,
            status=APPROVED
        )

        # 3) 2 that are in past (one cancelled)
        # study_user_event_registration_5
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_9_apply_online_free_past_cancelled,
            status=APPROVED
        )
        # study_user_event_registration_6
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_6_apply_online_free_past,
            status=APPROVED
        )

        # 4) 1 that is declined and in the past
        # study_user_event_registration_7
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_15_register_physical_costs_past,
            status=declined
        )

        # FOR PARTICIPANT TO APPLY FOR
        # Event - apply - online and free
        event_17_apply_online_free_future = Event.objects.create(
            name='Code Club 4 Teachers',
            description=(
                'Whether you are an absolute beginner or someone who has dabbled with '
                'programming and coding. Our focus is on having fun while integrating '
                'Digital Technologies and Hangarau Matihiko into your classroom programme.'
                'Join Tim Harford and explore how to integrate digital technologies and '
                'computational thinking into curriculum areas and gain an understanding of '
                'the fundamentals of programming using age appropriate programming languages.'
            ),
            start=datetime.datetime(2023, 6, 1, 8, 0, 0),
            end=datetime.datetime(2023, 6, 1, 10, 0, 0),
            accessible_online=True,
            published=True,
            featured=False,
            registration_type=2,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
        )
        event_17_apply_online_free_future.participant_types.set(
            [
                participant_type_free_event_staff,
                participant_type_free_facilitator,
                participant_type_free_teacher
            ]
        )
        event_17_apply_online_free_future.save()

        # Event - register - in person and costs
        event_18_register_physical_costs_future = Event.objects.create(
            name="How to really get started with Physical Computing",
            description=(
                'Uai started out teaching Physical Computing because he doesn\'t say '
                'no to his students ideas. He’ll share his experiences and discoveries '
                'that his students uncovered as he approached teaching Physical Computing '
                'from an inquiry and play based approach.\n\n'
                'The meetup will be delivered in English and will cater for all participants. '
                'We invite all Māori and English Medium kaiako to attend as the skills and '
                'knowledge covered in these sessions are relevant to both contexts.'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 6, 24),
            end=datetime.datetime(2023, 6, 26),
            accessible_online=False,
            published=True,
            featured=False,
            is_catered=True,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
        )
        event_18_register_physical_costs_future.locations.set([sample_location_2])
        event_18_register_physical_costs_future.participant_types.set(
            [
                participant_type_paid_event_staff,
                participant_type_paid_facilitator,
                participant_type_paid_teacher
            ]
        )
        event_18_register_physical_costs_future.save()

        # Event - register - in person and costs
        event_19 = Event.objects.create(
            name="Binary Counting for Beginners",
            description=(
                'This is open for all experience levels for learning about ,'
                'counting binary numbers or refeshing on how to count them.'
            ),
            registration_type=1,
            start=datetime.datetime(2023, 3, 15),
            end=datetime.datetime(2023, 3, 21),
            accessible_online=True,
            published=True,
            featured=False,
            is_catered=False,
            contact_email_address="eventstaff@event.co.nz",
            capacity=50
        )
        event_19.save()

        # Showing that user cannot withdraw from future event if declined
        EventRegistration.objects.create(
            participant_type=participant_type_free_event_staff,
            user=demo_user,
            representing="My school",
            event=event_19,
            status=declined
        )
