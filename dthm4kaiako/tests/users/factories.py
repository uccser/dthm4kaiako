"""Module for factories for tesing user application."""

from typing import Any, Sequence
from django.contrib.auth import get_user_model
import factory
from users.models import Entity


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for generating users."""

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        """Create password for user."""
        password = (
            extracted
            if extracted
            else factory.Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        """Metadata for UserFactory class."""

        model = get_user_model()


class EntityFactory(factory.django.DjangoModelFactory):
    """Factory for generating entities."""

    name = factory.Faker('company')
    url = factory.Faker('url')

    class Meta:
        """Metadata for class."""

        model = Entity
