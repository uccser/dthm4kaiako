from django.views import generic
from django.utils import timezone
from dtta.models import NewsArticle


class IndexView(generic.base.TemplateView):
    """View for DTTA homepage."""

    template_name = 'dtta/index.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the DTTA index view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['latest_news_articles'] = NewsArticle.objects.filter(datetime__lte=now).order_by('-datetime')
        return context


class NewsArticleDetailView(generic.DetailView):
    """View for DTTA news article."""

    model = NewsArticle
    context_object_name = 'news_article'
