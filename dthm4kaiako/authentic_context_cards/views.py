"""Views for authentic context cards application."""

from random import randint
from django.views import generic
from django.conf import settings
from django.db.models import Count
from authentic_context_cards.models import AchievementObjective

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
        achievement_objectives = AchievementObjective.objects.all()
        random_card = randint(0, len(achievement_objectives))
        context['achievement_objective'] = achievement_objectives[random_card]
        context['filename'] = settings.AUTHENTIC_CONTEXT_CARDS_FILENAME_TEMPLATE.replace(' ', '%20').split('{}')
        context['levels'] = AchievementObjective.objects.order_by(
            'level').values('level').annotate(count=Count('level'))
        return context
