"""Module for the custom Django sample_data command."""

import csv
import random
from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from tests.users.factories import EntityFactory
import datetime
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
)
# Events
from events.models import (
    Location,
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
from utils.new_zealand_regions import REGION_CHOICES


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
        DietaryRequirement.objects.create(name="None")
        DietaryRequirement.objects.create(name="Dairy free")
        DietaryRequirement.objects.create(name="Gluten free")
        DietaryRequirement.objects.create(name="Vegetarian")
        DietaryRequirement.objects.create(name="Vegan")
        DietaryRequirement.objects.create(name="Paleo")
        DietaryRequirement.objects.create(name="FODMAP")
        DietaryRequirement.objects.create(name="Nut allergies")
        DietaryRequirement.objects.create(name="Fish and shellfish allergies")
        DietaryRequirement.objects.create(name="Keto")
        DietaryRequirement.objects.create(name="Halal")
        DietaryRequirement.objects.create(name="As long as there's coffee, I'm happy!")
        print('Dietary requirements created.')


        # -------------------------- Realistic events for informal demonstrations --------------------------
        #TODO: finish creating realistic events

        # sample_location_1 = Location.objects.create(name='University of Canterbury', suburb='Ilam', city='Christchurch', region='14',coords=Point(-43,172))
        # sample_location_2 = Location.objects.create(
        #     room='Room 456',
        #     name='Middleton Grange School',
        #     street_address='12 High Street',
        #     suburb='Riccarton',
        #     city='Chrirstchurch',
        #     region=14,
        #     coords=Point(-12,149)
        # )

        # sample_location_3 = Location.objects.create(
        #     room='Room 7',
        #     name='Middleton Grange School',
        #     street_address='12 High Street',
        #     suburb='Riccarton',
        #     city='Chrirstchurch',
        #     region=14,
        #     coords=Point(-27,188)
        # )

        # sample_location_1.save()
        # sample_location_2.save()
        # sample_location_3.save()

        # sample_event_free_1 = Event.objects.create(name='DTHM for Kaiako Conference 2021',
        #                                      description='Inspirational collaboration to build your confidence teaching DT & HM.\n\n'
        #                                      + 'This is a FREE face to face Digital Technologies Teachers Aotearoa (DTTA) subject association event, for all teachers in Aotearoa. It\'s all about building your practice as a kaiako, for your learners.\n\n'
        #                                      + 'Join us for 3 days of:\n\n'
        #                                      + 'Connecting and reconnecting with colleagues across Aotearoa\n\n'
        #                                      + 'Engaging with a team to uncover and bring to light inspirational learning resources\n\n'
        #                                      + 'Developing programmes of learning that you will confidently take into your classroom and use immediately',
        #                                      start=datetime.datetime(2023, 4, 23, 8, 0, 0),
        #                                      end=datetime.datetime(2023, 4, 23, 8, 0, 0),
        #                                      published=True,
        #                                      featured=True,
        #                                      price=0,
        #                                      )
        
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

        # #TODO: free and paid events


        # --------------------------------------------------------------------------------------------------


        # Create common participant types
        ParticipantType.objects.create(name="Event staff")
        ParticipantType.objects.create(name="Teacher")
        ParticipantType.objects.create(name="Student")
        ParticipantType.objects.create(name="Facilitator")


        User = get_user_model()

        # Create admin account
        admin = User.objects.create_superuser(
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
        user = User.objects.create_user(
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
        print('User created.')

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
