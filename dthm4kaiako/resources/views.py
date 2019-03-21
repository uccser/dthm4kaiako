"""Views for resource application."""

from django.views import generic
from haystack.generic_views import SearchView
from rest_framework import viewsets
from utils.mixins import RedirectToCosmeticURLMixin
from resources.serializers import ResourceSerializer
from resources.models import (
    Resource,
    ResourceComponent,
    Language,
)
from resources.forms import ResourceSearchForm


class ResourceHomeView(generic.TemplateView):
    """View for home of resources."""

    template_name = 'resources/home.html'

    def get_context_data(self, **kwargs):
        """Provide the context data for the resource list view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['resource_count'] = Resource.objects.filter(published=True).count()
        context['resource_component_count'] = ResourceComponent.objects.filter(resource__published=True).count()
        context['languages'] = Language.objects.all()
        context['latest_resources'] = Resource.objects.filter(published=True).order_by(
            '-datetime_added').prefetch_related(
            'progress_outcomes',
            'year_levels',
            'technological_areas',
            'languages',
            'nzqa_standards',
            'curriculum_learning_areas',
        )[:10]
        return context


class ResourceDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a resource."""

    context_object_name = 'resource'

    def get_queryset(self, **kwargs):
        """Return queryset of resources to pull from."""
        return Resource.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        """Provide the context data for the resource detail view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['components'] = self.object.components.order_by('name')
        context['components_of'] = self.object.component_of.order_by('name')
        return context


class ResourceSearchView(SearchView):
    """View for resource search."""

    template_name = 'resources/search.html'
    form_class = ResourceSearchForm
    load_all = False

    def get_context_data(self, *args, **kwargs):
        """Return context dictionary for resource search view.

        Returns:
            Dictionary of context values.
        """
        context = super().get_context_data(*args, **kwargs)
        context['search'] = bool(self.request.GET)
        return context


class ResourceAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows resources to be viewed."""

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
