"""Base test class with methods implemented for Django testing."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import activate

User = get_user_model()


class BaseTestWithDB(TestCase):
    """Base test class with methods implemented for Django testing."""

    def __init__(self, *args, **kwargs):
        """Create a BaseTestWithDB object."""
        super().__init__(*args, **kwargs)
        self.language = None

    @classmethod
    def setUpTestData(cls):
        """Create data for the whole class.

        Creates a new user.
        """
        super(BaseTestWithDB, cls).setUpTestData()

    @classmethod
    def setUpClass(cls):
        """Automatically called before tests in class."""
        super(BaseTestWithDB, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Automatically called after tests in class."""
        super(BaseTestWithDB, cls).tearDownClass()

    def setUp(self):
        """Automatically called before each test.
        """
        if self.language is not None:
            activate(self.language)

    def tearDown(self):
        """Automatically called after each test."""
        pass
