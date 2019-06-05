"""Views for authentic context cards application."""

from random import randint
from django.views import generic
from django.conf import settings
from django.db.models import Count
from authentic_context_cards.models import (
    AchievementObjective,
    ProgressOutcome,
)
from authentic_context_cards.utils import get_card_set_metadata


RESPONSE_CONTENT_DISPOSITION = "attachment; filename*=UTF-8''{filename}.pdf; filename=\"{filename}.pdf\""


class HomeView(generic.base.TemplateView):
    """View for authentic context cards homepage."""

    template_name = 'authentic_context_cards/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the authentic context cards home view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)

        # Random Achievement Objective card
        achievement_objectives = AchievementObjective.objects.all()
        if achievement_objectives:
            random_card = randint(0, len(achievement_objectives))
            context['achievement_objective'] = achievement_objectives[random_card]

        # Random Progress Outcome card
        progress_outcomes = ProgressOutcome.objects.all()
        if progress_outcomes:
            random_card = randint(0, len(progress_outcomes))
            context['progress_outcome'] = progress_outcomes[random_card]

        # Begin card sets with achievement objectives sets
        achievement_objective_card_sets = list(AchievementObjective.objects.order_by(
            'level').values('level').annotate(count=Count('level')))
        card_set_type = 'ao'
        for card_set in achievement_objective_card_sets:
            for print_type in settings.AUTHENTIC_CONTEXT_CARDS_PRINT_TYPES:
                (title, filename) = get_card_set_metadata(
                    card_type=card_set_type,
                    print_type=print_type,
                    level=card_set['level'],
                    quote=True,
                )
                card_set['{}_filename'.format(print_type.lower())] = filename
            card_set['type'] = card_set_type
            card_set['title'] = title

        # Add progress outcome card sets
        progress_outcome_card_sets = list(ProgressOutcome.objects.order_by(
            'learning_area').values('learning_area').annotate(count=Count('learning_area')))
        card_set_type = 'po'
        for card_set in progress_outcome_card_sets:
            for print_type in settings.AUTHENTIC_CONTEXT_CARDS_PRINT_TYPES:
                (title, filename) = get_card_set_metadata(
                    card_type=card_set_type,
                    print_type=print_type,
                    learning_area=card_set['learning_area'],
                    quote=True,
                )
                card_set['{}_filename'.format(print_type.lower())] = filename
            card_set['type'] = card_set_type
            card_set['title'] = title

        context['card_sets'] = progress_outcome_card_sets + achievement_objective_card_sets
        return context
