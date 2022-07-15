from django.test import TestCase
from django.http import HttpRequest

from users.forms import SignupForm, UserChangeForm, UserCreationForm, UserUpdateDetailsForm
from users.models import User, DietaryRequirement

from tests.dthm4kaiako_test_data_generator import generate_dietary_requirements

class UserUpdateDetailsFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request = HttpRequest()
        cls.user = User.objects.create_user(
            username="Johnny",
            email="testing@testing.com",
            password="poorpassword123"
            )

    def test_all_fields_present(self):

        form = UserUpdateDetailsForm()
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("region", form.fields)
        self.assertIn("mobile_phone_number", form.fields)
        self.assertIn("educational_entities", form.fields)
        self.assertIn("medical_notes", form.fields)
        self.assertIn("dietary_requirements", form.fields)

    def test_form_hides_dietary_requirements_field_for_non_catered_event(self):

        show_dietary_requirements = False
        initial_data={'show_dietary_requirements': show_dietary_requirements}

        self.request.POST = {
            "user": self.user.pk,
            "first_name": "Johnny",
            "last_name": "Daniels",
            "region": 1,
            "mobile_phone_number": "123456789",
            "educational_entities": "",
            "medical_notes": "",
        }

        form = UserUpdateDetailsForm(self.request.POST, initial=initial_data)
        self.assertNotIn("dietary_requirements", form.fields)

    def test_form_shows_dietary_requirements_field_for_catered_event(self):

        generate_dietary_requirements()

        show_dietary_requirements = True
        initial_data={'show_dietary_requirements': show_dietary_requirements}

        self.request.POST = {
            "user": self.user.pk,
            "first_name": "Johnny",
            "last_name": "Daniels",
            "region": 1,
            "mobile_phone_number": "123456789",
            "educational_entities": "",
            "medical_notes": "",
            "dietary_requirements": ["Vegan"]
        }

        form = UserUpdateDetailsForm(self.request.POST, initial=initial_data)
        self.assertIn("dietary_requirements", form.fields)

        