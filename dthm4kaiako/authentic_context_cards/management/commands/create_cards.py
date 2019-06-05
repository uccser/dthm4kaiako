"""Module for the custom Django create_cards command."""

import os
from django.core import management
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from authentic_context_cards.models import (
    AchievementObjective,
    ProgressOutcome,
)
from authentic_context_cards.utils import get_card_set_metadata
from weasyprint import HTML, CSS


class Command(management.base.BaseCommand):
    """Required command class for the custom Django create_cards command."""

    help = 'Create authentic context card PDFs for each level.'

    def handle(self, *args, **options):
        """Automatically called when the create_cards command is given."""
        pdf_directory = settings.AUTHENTIC_CONTEXT_CARDS_GENERATION_LOCATION
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory)
        self.create_achievement_objective_cards(pdf_directory)
        self.create_progress_outcome_cards(pdf_directory)

    def create_achievement_objective_cards(self, pdf_directory):
        """Create achievement objective cards.

        Args:
            pdf_directory (str): Path to write files to.
        """
        achievement_objectives_level_values = AchievementObjective.objects.all().values_list(
            'level', flat=True).order_by('level').distinct()
        card_type = 'ao'
        for level_num in achievement_objectives_level_values:
            for print_type in settings.AUTHENTIC_CONTEXT_CARDS_PRINT_TYPES:
                (title, filename) = get_card_set_metadata(
                    card_type=card_type,
                    print_type=print_type,
                    level=level_num,
                    quote=False,
                )
                objectives = AchievementObjective.objects.filter(level=level_num).order_by('code')

                context = dict()
                context['print_type'] = print_type
                context['filename'] = filename
                context['card_type'] = card_type
                context['cards'] = self.prepare_card_data(objectives, print_type)
                self.write_card_pdf(pdf_directory, filename, context)
                print('Created {}'.format(filename))

    def create_progress_outcome_cards(self, pdf_directory):
        """Create progress outcome cards.

        Args:
            pdf_directory (str): Path to write files to.
        """
        learning_areas = ProgressOutcome.objects.all().values_list(
            'learning_area', flat=True).distinct()
        card_type = 'po'
        for learning_area in learning_areas:
            for print_type in settings.AUTHENTIC_CONTEXT_CARDS_PRINT_TYPES:
                (title, filename) = get_card_set_metadata(
                    card_type=card_type,
                    print_type=print_type,
                    learning_area=learning_area,
                    quote=False,
                )
                outcomes = ProgressOutcome.objects.filter(learning_area=learning_area).order_by('code')

                context = dict()
                context['print_type'] = print_type
                context['filename'] = filename
                context['card_type'] = card_type
                context['cards'] = self.prepare_card_data(outcomes, print_type)
                self.write_card_pdf(pdf_directory, filename, context)
                print('Created {}'.format(filename))

    def prepare_card_data(self, items, print_type):
        """Prepare card data for rendering."""
        cards = list()
        if print_type == settings.AUTHENTIC_CONTEXT_CARDS_SINGLE_PRINT:
            for item in items:
                cards.append(
                    {
                        'item': item,
                        'side': 'back',
                    }
                )
                cards.append(
                    {
                        'item': item,
                        'side': 'front',
                    }
                )
        else:
            items = list(items)
            cards_per_page = 4
            fronts = list()
            backs = list()
            blank_card = {
                'item': None,
                'side': 'back',
            }
            for item in items:
                backs.append(
                    {
                        'item': item,
                        'side': 'back',
                    }
                )
                fronts.append(
                    {
                        'item': item,
                        'side': 'front',
                    }
                )
                if len(fronts) == 4 or item == items[-1]:
                    blanks = list()
                    for i in range(cards_per_page - len(fronts)):
                        blanks.append(blank_card)
                    cards.extend(backs)
                    cards.extend(blanks)
                    if len(fronts) == 1:
                        cards.append(blanks.pop())
                        cards.extend(fronts)
                        cards.extend(blanks)
                    elif len(fronts) == 2:
                        cards.append(fronts.pop(1))
                        cards.append(fronts.pop(0))
                        cards.extend(blanks)
                    elif len(fronts) == 3:
                        cards.append(fronts.pop(0))
                        cards.append(fronts.pop(0))
                        cards.append(blanks.pop())
                        cards.extend(fronts)
                        cards.extend(blanks)
                    else:
                        cards.append(fronts.pop(1))
                        cards.append(fronts.pop(0))
                        cards.append(fronts.pop(1))
                        cards.append(fronts.pop(0))
                    backs = list()
                    fronts = list()
        return cards

    def write_card_pdf(self, pdf_directory, filename, context):
        """Write card PDF to directory.

        Args:
            pdf_directory (str): Path to write files to.
            filename (str): Filename of file to write.
            context (dict): Context used for rendering template.

        """
        pdf_html = render_to_string('authentic_context_cards/cards-pdf.html', context)
        html = HTML(string=pdf_html, base_url=settings.BUILD_ROOT)

        # Render as PDF
        css_file = finders.find('css/authentic-context-cards.css')
        css_string = open(css_file, encoding='UTF-8').read()
        base_css = CSS(string=css_string)
        pdf_file = html.write_pdf(stylesheets=[base_css])

        # Save file
        pdf_file_output = open(os.path.join(pdf_directory, filename), 'wb')
        pdf_file_output.write(pdf_file)
        pdf_file_output.close()
