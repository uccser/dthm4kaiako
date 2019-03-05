"""Module for the custom Django sampledata command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from allauth.account.models import EmailAddress
from resources.models import (
    Language,
    TechnologicalArea,
    ProgressOutcome,
    YearLevel,
    CurriculumLearningArea,
)
from events.models import (
    Location,
    Series,
)
from tests.resources.factories import (
    ResourceFactory,
    NZQAStandardFactory,
)
from tests.events.factories import (
    SponsorFactory,
    OrganiserFactory,
    EventFactory,
)
from tests.dtta.factories import (
    NewsArticleFactory,
    PageFactory,
    RelatedLinkFactory,
)


class Command(management.base.BaseCommand):
    """Required command class for the custom Django sampledata command."""

    help = "Add sample data to database."

    def handle(self, *args, **options):
        """Automatically called when the sampledata command is given."""
        if settings.DEPLOYMENT_TYPE == 'prod' and not settings.DEBUG:
            raise management.base.CommandError(
                'This command can only be executed in DEBUG mode on non-production website.'
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
        SponsorFactory.create_batch(size=10)
        print('Event sponsors created.')
        OrganiserFactory.create_batch(size=10)
        print('Event organisers created.')
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
            (
                'Kia Takatū ā-Matihiko Webinars',
                'KTAM Webinars',
            ),
        }
        for (name, abbreviation) in event_series:
            Series.objects.create(
                name=name,
                abbreviation=abbreviation,
            )
        print('Event series created.')
        event_locations = {
            # Name, Latitude, Longitude
            (
                "Erskine Building, University of Canterbury, Christchurch",
                -43.52257394343779,
                172.58110338161464,
            ),
            (
                "Central Lecture Theatres, University of Canterbury, Christchurch",
                -43.523110727405,
                172.58360856483455,
            ),
            (
                "Burnside High School, Christchurch",
                -43.50806966261862,
                172.57665261421835,
            ),
            (
                "Hobsonville Point Secondary School, 70 Hobsonville Point Road, Auckland",
                -36.795041366345274,
                174.65528011322021,
            ),
            (
                "Wellington Girls' College, Wellington",
                -41.275429,
                174.780210,
            ),
            (
                "Western Springs College, Western Springs, Auckland",
                -36.861982,
                174.717508,
            ),
            (
                "St Peter’s College, Milson, Palmerston North",
                -40.334277,
                175.605451,
            ),
            (
                "Southland Girls' High School, Georgetown, Invercargill",
                -46.417670,
                168.365330,
            ),
        }
        for (name, lat, lng) in event_locations:
            Location.objects.create(
                name=name,
                description=name,
                coords=Point(lng, lat),
            )
        print('Event locations created.')
        EventFactory.create_batch(size=30)
        print('Events created.')

        # DTTA
        NewsArticleFactory.create_batch(size=20)
        print('DTTA news articles created.')
        PageFactory.create_batch(size=5)
        print('DTTA pages created.')
        RelatedLinkFactory.create_batch(size=10)
        print('DTTA related links created.')
