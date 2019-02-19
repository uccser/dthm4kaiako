"""Views for resource application."""

from django.views import generic
from django.db.models import Count
from rest_framework import viewsets
from utils.mixins import RedirectToCosmeticURLMixin
from resources.serializers import ResourceSerializer
from resources.models import (
    Resource,
    ResourceComponent,
    Language,
)


class ResourceListView(generic.ListView):
    """View for listing resources."""

    queryset = Resource.objects.order_by('name').annotate(Count('components')).prefetch_related(
        'progress_outcomes',
        'year_levels',
        'technology_curriculum_strands',
        'languages',
        'nzqa_standards',
        'curriculum_learning_areas',
    )
    context_object_name = 'resources'

    def get_context_data(self, **kwargs):
        """Provide the context data for the resource list view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['resource_count'] = Resource.objects.count()
        context['resource_component_count'] = ResourceComponent.objects.count()
        context['languages'] = Language.objects.all()
        return context


class ResourceDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a resource."""

    model = Resource
    context_object_name = 'resource'

    def get_context_data(self, **kwargs):
        """Provide the context data for the resource detail view.

        Returns:
            Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['components'] = self.object.components.order_by('name')
        context['components_of'] = self.object.component_of.order_by('name')
        return context


class ResourceAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows resources to be viewed."""

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
