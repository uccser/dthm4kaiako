"""Module for factories for tesing user application."""

from typing import Any, Sequence
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation


class UserFactory(DjangoModelFactory):
    """Factory for generating users."""

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        """Create password for user."""
        password = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(
            extra_kwargs={}
        )
        self.set_password(password)

    class Meta:
        """Metadata for UserFactory class."""

        model = get_user_model()
        django_get_or_create = ["username"]
