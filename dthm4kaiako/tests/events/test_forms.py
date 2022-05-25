from django.test import TestCase
from events.forms import EventApplicationForm, TermsAndConditionsForm

class EventApplicationForm(TestCase):
    @classmethod
    def setUpTestData(cls):


    def test_required_fields_only(self):

         #TODO: figure out how to represent the applicant type
         form_data = {
             
         }

         form = EventApplicationForm(data=form_data)

         self.assertTrue(form.is_valid())