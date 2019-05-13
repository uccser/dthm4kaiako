"""Views for DTTA application."""

from django.views import generic
from django.utils.timezone import now
from datetime import timedelta
from utils.mixins import RedirectToCosmeticURLMixin
from dtta.models import (
    Page,
    Project,
    NewsArticle,
    RelatedLink,
)


class HomeView(generic.base.TemplateView):
    """View for DTTA homepage."""

    template_name = 'dtta/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the DTTA index view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        last_month = now() - timedelta(days=30)
        context['latest_news_articles'] = NewsArticle.objects.filter(
            datetime__lte=now()).filter(datetime__gte=last_month).order_by('-datetime')
        context['related_links'] = RelatedLink.objects.order_by('order_number')
        return context


class AboutView(generic.base.TemplateView):
    """View for DTTA about page."""

    template_name = 'dtta/about.html'


class MembershipView(generic.base.TemplateView):
    """View for DTTA membership page."""

    template_name = 'dtta/membership.html'


class PageDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for DTTA flat page."""

    model = Page
    context_object_name = 'page'

    def get_queryset(self):
        """Only show published pages.

        Returns:
            Pages filtered by published boolean.
        """
        return Page.objects.filter(published=True)


class ProjectDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for DTTA project page."""

    model = Project
    context_object_name = 'project'

    def get_queryset(self):
        """Only show published project pages.

        Returns:
            Project pages filtered by published boolean.
        """
        return Project.objects.filter(published=True)


class NewsArticleListView(generic.ListView):
    """View for listing DTTA news articles."""

    model = NewsArticle
    context_object_name = 'news_articles'

    def get_queryset(self):
        """Only show articles before or equal to the current datetime.

        Returns:
            News articles filtered by current datetime.
        """
        return NewsArticle.objects.filter(datetime__lte=now()).order_by(
            '-datetime').prefetch_related('audiences').select_related('source')


class NewsArticleDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for DTTA news article."""

    model = NewsArticle
    context_object_name = 'news_article'

    def get_queryset(self):
        """Only show articles before or equal to the current datetime.

        Returns:
            News articles filtered by current datetime.
        """
        return NewsArticle.objects.filter(datetime__lte=now())
