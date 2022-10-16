"""Unit tests for convert_string_list_to_one_string view helper function"""

from events.views import convert_string_list_to_one_string
from tests.BaseTestWithDB import BaseTestWithDB


class ConvertStringListToOneStringTest(BaseTestWithDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_convert_string_list_to_one_string_empty_list(self):
        test_list = []
        expected_result = ""
        self.assertEqual(expected_result, convert_string_list_to_one_string(test_list))

    def test_convert_string_list_to_one_string_one_item_in_list(self):
        test_list = ["Gluten-free"]
        expected_result = "Gluten-free"
        self.assertEqual(expected_result, convert_string_list_to_one_string(test_list))

    def test_convert_string_list_to_one_string_many_items_list(self):
        test_list = ["Gluten-free", "Vegan", "Dairy-free"]
        expected_result = "Gluten-free & Vegan & Dairy-free"
        self.assertEqual(expected_result, convert_string_list_to_one_string(test_list))
