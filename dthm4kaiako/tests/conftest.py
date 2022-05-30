"""Module for configuring pytest."""

import pytest
from django.test import RequestFactory
from django.core import management
from tests.users.factories import UserFactory
from users.models import User


@pytest.fixture
def user(request):
    """Pytest setup for user model."""
    management.call_command('load_user_types')

    def fin():
        print("teardown")
        User.objects.all().delete()

    request.addfinalizer(fin)
    return UserFactory()


@pytest.fixture
def request_factory():
    """Pytest setup for factory."""
    return RequestFactory()