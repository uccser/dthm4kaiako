"""Module for the custom Django sampledata command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from resources.models import (
    Language,
    TechnologyCurriculumStrand,
    ProgressOutcome,
    YearLevel,
)
from tests.resources.factories import (
    ResourceFactory,
    NZQAStandardFactory,
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
        if not settings.DEBUG:
            raise management.base.CommandError(
                'This command can only be executed in DEBUG mode.'
            )

        # Clear all data
        management.call_command('flush', interactive=False)

        User = get_user_model()

        # Create admin account
        admin = User.objects.create_superuser(
            'admin',
            'admin@dthm4kaiako.ac.nz',
            'password',
            first_name='Admin',
            last_name='Account'
        )
        EmailAddress.objects.create(
            user=admin,
            email=admin.email,
            primary=True,
            verified=True
        )

        # Create user account
        alex = User.objects.create_user(
            'user',
            'user@dthm4kaiako.ac.nz',
            password='password',
            first_name='Alex',
            last_name='Doe'
        )
        EmailAddress.objects.create(
            user=alex,
            email=alex.email,
            primary=True,
            verified=True
        )

        # Resources
        Language.objects.create(name='English', css_class='lang-en')
        Language.objects.create(name='Māori', css_class='lang-mi')
        tcs_ct = TechnologyCurriculumStrand.objects.create(
            name='Computational thinking',
            abbreviation='CT',
            css_class='tcs-ct',
        )
        for i in range(1, 9):
            ProgressOutcome.objects.create(
                name='Computational thinking - Progress outcome {}'.format(i),
                abbreviation='CT PO{}'.format(i),
                technology_curriculum_strand=tcs_ct,
                css_class='po-ct',
            )
        tcs_dddo = TechnologyCurriculumStrand.objects.create(
            name='Designing and developing digital outcomes',
            abbreviation='DDDO',
            css_class='tcs-dddo',
        )
        for i in range(1, 7):
            ProgressOutcome.objects.create(
                name='Designing and developing digital outcomes - Progress outcome {}'.format(i),
                abbreviation='DDDO PO{}'.format(i),
                technology_curriculum_strand=tcs_dddo,
                css_class='po-dddo',
            )
        NZQAStandardFactory.create_batch(size=20)
        for i in range(0, 14):
            YearLevel.objects.create(
                level=i
            )
        ResourceFactory.create_batch(size=50)

        # DTTA
        NewsArticleFactory.create_batch(size=20)
        PageFactory.create_batch(size=5)
        RelatedLinkFactory.create_batch(size=10)
