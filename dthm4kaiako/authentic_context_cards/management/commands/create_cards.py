"""Module for the custom Django create_cards command."""

import os
from django.core import management
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from authentic_context_cards.models import AchievementObjective
from weasyprint import HTML, CSS


class Command(management.base.BaseCommand):
    """Required command class for the custom Django create_cards command."""

    help = 'Create authentic context card PDFs for each level.'

    def add_arguments(self, parser):
        """Add optional parameter to create_cards command."""
        parser.add_argument(
            "level_number",
            nargs="?",
            default=None,
            help="The level of cards to generate",
        )

    def handle(self, *args, **options):
        """Automatically called when the create_cards command is given."""
        pdf_directory = settings.AUTHENTIC_CONTEXT_CARDS_GENERATION_LOCATION
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory)

        if options["level_number"]:
            level_values = [int(options["level_number"])]
        else:
            level_values = AchievementObjective.objects.all().values_list(
                'level', flat=True).order_by('level').distinct()

        for level_num in level_values:
            for print_type in settings.AUTHENTIC_CONTEXT_CARDS_PRINT_TYPES:
                context = dict()
                context['print_type'] = print_type

                # Create filename
                filename = settings.AUTHENTIC_CONTEXT_CARDS_FILENAME_TEMPLATE.format(level_num, print_type)
                context['filename'] = filename

                # Create card data
                cards = list()
                objectives = AchievementObjective.objects.filter(level=level_num).order_by('code')
                if print_type == settings.AUTHENTIC_CONTEXT_CARDS_SINGLE_PRINT:
                    for objective in objectives:
                        cards.append(
                            {
                                'objective': objective,
                                'side': 'back',
                            }
                        )
                        cards.append(
                            {
                                'objective': objective,
                                'side': 'front',
                            }
                        )
                else:
                    objectives = list(objectives)
                    cards_per_page = 4
                    fronts = list()
                    backs = list()
                    blank_card = {
                        'objective': None,
                        'side': 'back',
                    }
                    for objective in objectives:
                        backs.append(
                            {
                                'objective': objective,
                                'side': 'back',
                            }
                        )
                        fronts.append(
                            {
                                'objective': objective,
                                'side': 'front',
                            }
                        )
                        if len(fronts) == 4 or objective == objectives[-1]:
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

                # Create HTML
                context['cards'] = cards
                pdf_html = render_to_string('authentic_context_cards/cards-pdf.html', context)
                html = HTML(string=pdf_html, base_url=settings.BUILD_ROOT)

                # Render as PDF
                css_file = finders.find('css/authentic-context-cards.css')
                css_string = open(css_file, encoding='UTF-8').read()
                base_css = CSS(string=css_string)
                pdf_file = html.write_pdf(stylesheets=[base_css])

                # Save file
                filename = '{}.pdf'.format(filename)
                pdf_file_output = open(os.path.join(pdf_directory, filename), 'wb')
                pdf_file_output.write(pdf_file)
                pdf_file_output.close()

                print('Created {}'.format(filename))
