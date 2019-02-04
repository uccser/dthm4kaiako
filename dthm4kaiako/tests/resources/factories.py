"""Module for factories for tesing resources application."""

import random
from factory import DjangoModelFactory, Faker, post_generation
from factory.faker import faker
from resources.models import (
    Resource,
    ResourceComponent,
)


class ResourceFactory(DjangoModelFactory):
    """Factory for generating resources."""

    name = Faker('sentence')
    description = Faker('paragraph', nb_sentences=5)

    class Meta:
        """Metadata for class."""

        model = Resource

    @post_generation
    def create_components(self, create, extracted, **kwargs):
        FAKER = faker.Faker()
        number_of_components = random.randint(0, 9)
        for i in range(number_of_components):

            component_name = FAKER.sentence()
            component_type = random.choice(list(ResourceComponent.COMPONENT_TYPE_DATA))
            if component_type == ResourceComponent.TYPE_WEBSITE:
                ResourceComponent.objects.create(
                    name=component_name,
                    resource=self,
                    component_url=FAKER.url(),
                )
            # TODO: Implement all types of components
            else:
                ResourceComponent.objects.create(
                    name=component_name,
                    resource=self,
                    component_url=FAKER.url(),
                )
