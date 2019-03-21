"""Views for authentic context cards application."""

from random import randint
from django.views import generic
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Count
from django.template.loader import render_to_string
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
        context['achievement_outcome'] = achievement_objectives[random_card]
        context['filename'] = settings.AUTHENTIC_CONTEXT_CARDS_FILENAME_TEMPLATE[:-2].replace(' ', '%20')
        context['levels'] = AchievementObjective.objects.order_by(
            'level').values('level').annotate(count=Count('level'))
        return context


def generate_cards(request):
    """View for generated PDF of a specific cards.

    Args:
        request: HttpRequest object.

    Returns:
        HTML response containing PDF of cards.
    """
    from weasyprint import HTML, CSS
    context = dict()
    context["achievement_outcomes"] = AchievementObjective.objects.all()[:10]

    filename = "{} ({})".format('Authentic Context Cards', 'Random 10 cards')
    context["filename"] = filename

    pdf_html = render_to_string("authentic_context_cards/card-pdf.html", context)
    html = HTML(string=pdf_html, base_url=settings.BUILD_ROOT)
    # css_file = finders.find("css/print-resource-pdf.css")
    # css_string = open(css_file, encoding="UTF-8").read()
    css_string = ''
    base_css = CSS(string=css_string)
    pdf_file = html.write_pdf(stylesheets=[base_css])
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = RESPONSE_CONTENT_DISPOSITION.format(filename=filename)
    return response
