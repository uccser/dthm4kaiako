"""Test class for search_utils module."""

from tests.BaseTestWithDB import BaseTestWithDB
from utils import search_utils
from resources.models import (
    TechnologicalArea,
    ProgressOutcome,
)


class ConcatFieldValuesTest(BaseTestWithDB):
    """Test class for concat_field_values module."""

    def test_concat_field_values_one_queryset_one_field(self):
        TechnologicalArea.objects.create(
            name='techarea-1',
            abbreviation='ta-1',
            css_class='ta-css-1',
        )
        TechnologicalArea.objects.create(
            name='techarea-2',
            abbreviation='ta-2',
            css_class='ta-css-2',
        )
        TechnologicalArea.objects.create(
            name='techarea-3',
            abbreviation='ta-3',
            css_class='ta-css-3',
        )
        qs1 = TechnologicalArea.objects.values_list('name')
        self.assertEqual(
            search_utils.concat_field_values(qs1),
            'techarea-1 techarea-2 techarea-3'
        )

    def test_concat_field_values_one_queryset_multiple_fields(self):
        TechnologicalArea.objects.create(
            name='techarea-1',
            abbreviation='ta-1',
            css_class='ta-css-1',
        )
        TechnologicalArea.objects.create(
            name='techarea-2',
            abbreviation='ta-2',
            css_class='ta-css-2',
        )
        TechnologicalArea.objects.create(
            name='techarea-3',
            abbreviation='ta-3',
            css_class='ta-css-3',
        )
        qs1 = TechnologicalArea.objects.values_list('name', 'abbreviation')
        self.assertEqual(
            search_utils.concat_field_values(qs1),
            'techarea-1 ta-1 techarea-2 ta-2 techarea-3 ta-3'
        )

    def test_concat_field_values_multiple_querysets_one_field(self):
        ta1 = TechnologicalArea.objects.create(
            name='techarea-1',
            abbreviation='ta-1',
            css_class='ta-css-1',
        )
        ta2 = TechnologicalArea.objects.create(
            name='techarea-2',
            abbreviation='ta-2',
            css_class='ta-css-2',
        )
        TechnologicalArea.objects.create(
            name='techarea-3',
            abbreviation='ta-3',
            css_class='ta-css-3',
        )
        qs1 = TechnologicalArea.objects.values_list('name')
        ProgressOutcome.objects.create(
            name='progressoutcome-1',
            abbreviation='po-1',
            technological_area=ta1,
            css_class='po-css-1',
        )
        ProgressOutcome.objects.create(
            name='progressoutcome-2',
            abbreviation='po-2',
            technological_area=ta2,
            css_class='po-css-2',
        )
        qs2 = ProgressOutcome.objects.values_list('name')
        self.assertEqual(
            search_utils.concat_field_values(qs1, qs2),
            'techarea-1 techarea-2 techarea-3 progressoutcome-1 progressoutcome-2'
        )

    def test_concat_field_values_multiple_querysets_multiple_fields(self):
        ta1 = TechnologicalArea.objects.create(
            name='techarea-1',
            abbreviation='ta-1',
            css_class='ta-css-1',
        )
        ta2 = TechnologicalArea.objects.create(
            name='techarea-2',
            abbreviation='ta-2',
            css_class='ta-css-2',
        )
        TechnologicalArea.objects.create(
            name='techarea-3',
            abbreviation='ta-3',
            css_class='ta-css-3',
        )
        qs1 = TechnologicalArea.objects.values_list('name', 'abbreviation')
        ProgressOutcome.objects.create(
            name='progressoutcome-1',
            abbreviation='po-1',
            technological_area=ta1,
            css_class='po-css-1',
        )
        ProgressOutcome.objects.create(
            name='progressoutcome-2',
            abbreviation='po-2',
            technological_area=ta2,
            css_class='po-css-2',
        )
        qs2 = ProgressOutcome.objects.values_list('name', 'css_class')
        self.assertEqual(
            search_utils.concat_field_values(qs1, qs2),
            'techarea-1 ta-1 techarea-2 ta-2 techarea-3 ta-3 progressoutcome-1 po-css-1 progressoutcome-2 po-css-2'
        )

    def test_concat_field_values_multiple_querysets_relationship_field(self):
        ta1 = TechnologicalArea.objects.create(
            name='techarea-1',
            abbreviation='ta-1',
            css_class='ta-css-1',
        )
        ta2 = TechnologicalArea.objects.create(
            name='techarea-2',
            abbreviation='ta-2',
            css_class='ta-css-2',
        )
        ProgressOutcome.objects.create(
            name='progressoutcome-1',
            abbreviation='po-1',
            technological_area=ta1,
            css_class='po-css-1',
        )
        ProgressOutcome.objects.create(
            name='progressoutcome-2',
            abbreviation='po-2',
            technological_area=ta2,
            css_class='po-css-2',
        )
        qs1 = ProgressOutcome.objects.values_list('name', 'technological_area__name')
        self.assertEqual(
            search_utils.concat_field_values(qs1),
            'progressoutcome-1 techarea-1 progressoutcome-2 techarea-2'
        )
