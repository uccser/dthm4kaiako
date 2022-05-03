"""Module for the custom Django sample_data command."""

import csv
import random
from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from allauth.account.models import EmailAddress
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
# Events
from events.models import (
    Location,
    Series,
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
        for (code, name) in Location.REGION_CHOICES:
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
