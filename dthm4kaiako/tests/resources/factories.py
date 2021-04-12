"""Module for factories for testing the resources application."""

import random
from django.contrib.auth import get_user_model
from factory import Faker, post_generation, LazyFunction
from factory.django import DjangoModelFactory
from factory.faker import faker
from resources.models import (
    Resource,
    ResourceComponent,
    Language,
    NZQAStandard,
    CurriculumLearningArea,
    TechnologicalArea,
    ProgressOutcome,
    YearLevel,
)
from users.models import Entity

CONTENT_PRIMARY = 1
CONTENT_SECONDARY = 2
CONTENT_BOTH = 3
User = get_user_model()


class NZQAStandardFactory(DjangoModelFactory):
    """Factory for generating NZQA standards."""

    name = Faker('sentence')
    abbreviation = LazyFunction(lambda: 'AS{}'.format(random.randint(10000, 99999)))
    level = LazyFunction(lambda: random.randint(1, 3))

    class Meta:
        """Metadata for class."""

        model = NZQAStandard


class CurriculumLearningAreaFactory(DjangoModelFactory):
    """Factory for generating curriculum learning areas."""

    name = Faker('word')
    css_class = 'cla'

    class Meta:
        """Metadata for class."""

        model = CurriculumLearningArea


class ResourceFactory(DjangoModelFactory):
    """Factory for generating resources."""

    name = Faker('sentence')
    description = Faker('paragraph', nb_sentences=5)
    published = True

    class Meta:
        """Metadata for class."""

        model = Resource

    @post_generation
    def add_detail(self, create, extracted, **kwargs):
        """Add detail to resource."""

        # Set language
        # 25% chance both languages, otherwise one
        if random.randint(1, 4) == 1:
            self.languages.add(*Language.objects.all())
        else:
            self.languages.add(random.choice(Language.objects.all()))

        # Set technological areas
        # 20% chance both, otherwise one
        if random.randint(1, 5) == 1:
            self.technological_areas.add(
                *TechnologicalArea.objects.all()
            )
        else:
            self.technological_areas.add(
                random.choice(TechnologicalArea.objects.all())
            )

        # Choose primary (45%), secondary (45%), both (10%) for rest of variables
        if random.randint(1, 10) == 1:
            resource_detail_content = CONTENT_BOTH
            self.year_levels.add(
                *random.sample(
                    list(YearLevel.objects.all()),
                    random.randint(1, 4)
                )
            )
        elif random.randint(1, 2) == 1:
            resource_detail_content = CONTENT_PRIMARY
            self.year_levels.add(
                *random.sample(
                    list(YearLevel.objects.filter(level__lte=8)),
                    random.randint(1, 4)
                )
            )
        else:
            resource_detail_content = CONTENT_SECONDARY
            self.year_levels.add(
                *random.sample(
                    list(YearLevel.objects.filter(level__gte=9)),
                    random.randint(1, 4)
                )
            )

        # Add progress outcomes
        if resource_detail_content in [CONTENT_BOTH, CONTENT_PRIMARY]:
            self.progress_outcomes.add(
                *random.sample(
                    list(ProgressOutcome.objects.filter(
                        technological_area__in=self.technological_areas.all()
                    )),
                    random.randint(1, 3)
                )
            )

        # Add NZQA standards
        if resource_detail_content in [CONTENT_BOTH, CONTENT_SECONDARY]:
            self.nzqa_standards.add(
                *random.sample(
                    list(NZQAStandard.objects.all()),
                    random.randint(1, 3)
                )
            )

        # Add curriculum learning areas
        self.curriculum_learning_areas.add(
            *random.sample(
                list(CurriculumLearningArea.objects.all()),
                random.randint(0, 2)
            )
        )

        # 60% chance entity authors only
        # 30% chance user authors only
        # 10% chance entity and user authors
        rand_author_int = random.randint(1, 10)
        if rand_author_int <= 6:
            add_entity_authors(self)
        elif rand_author_int <= 9:
            add_user_authors(self)
        else:
            add_entity_authors(self)
            add_user_authors(self)

        # Add components
        number_of_components = random.randint(1, 9)
        for i in range(number_of_components):
            component_name = faker.Faker().sentence()
            component_type = random.choice(list(ResourceComponent.COMPONENT_TYPE_DATA))
            resource_count = Resource.objects.count()

            if component_type == ResourceComponent.TYPE_RESOURCE and resource_count >= 2:
                resources = list(Resource.objects.exclude(pk=self.pk))
                resource_component = resources[random.randint(0, len(resources) - 1)]
                ResourceComponent.objects.create(
                    name=resource_component.name,
                    resource=self,
                    component_resource=resource_component,
                )
            # TODO: Implement all types of components
            else:  # Website
                ResourceComponent.objects.create(
                    name=component_name,
                    resource=self,
                    component_url=faker.Faker().url(),
                )


def add_entity_authors(self):
    """Set author entities."""
    # 80% chance one entity, otherwise multiple
    if random.randint(1, 5) == 1:
        self.author_entities.add(*random.sample(
            list(Entity.objects.all()),
            random.randint(2, 3)
        ))
    else:
        self.author_entities.add(random.choice(Entity.objects.all()))


def add_user_authors(self):
    """Set author user."""
    # 80% chance one user, otherwise multiple
    if random.randint(1, 5) == 1:
        self.author_users.add(*random.sample(
            list(User.objects.all()),
            random.randint(2, min(User.objects.count(), 4))
        ))
    else:
        self.author_users.add(random.choice(User.objects.all()))
