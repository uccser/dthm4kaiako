"""Module for the custom Django sampledata command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
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
from tests.events.factories import (
    SponsorFactory,
    LocationFactory,
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
        SponsorFactory.create_batch(size=6)
        print('Event sponsors created.')
        LocationFactory.create_batch(size=20)
        print('Event locations created.')

        # DTTA
        NewsArticleFactory.create_batch(size=20)
        print('DTTA news articles created.')
        PageFactory.create_batch(size=5)
        print('DTTA pages created.')
        RelatedLinkFactory.create_batch(size=10)
        print('DTTA related links created.')
