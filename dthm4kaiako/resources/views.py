"""Views for resource application."""

from django.views import generic
from django.db.models import (
    F,
    Value,
    BooleanField,
    Case,
    When,
)
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
)
from rest_framework import viewsets
from utils.mixins import RedirectToCosmeticURLMixin
from resources.serializers import ResourceSerializer
from resources.models import (
    Resource,
    ResourceComponent,
    Language,
    TechnologicalArea,
    ProgressOutcome,
    NZQAStandard,
    YearLevel,
    CurriculumLearningArea,
)


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
        context['author_count'] = self.object.author_entities.count() + self.object.author_users.count()
        context['components'] = self.object.components.order_by('name')
        context['components_of'] = self.object.component_of.order_by('name')
        return context


class ResourceSearchView(generic.TemplateView):
    """View for resource search."""

    template_name = 'resources/search.html'

    def get_context_data(self, *args, **kwargs):
        """Return context dictionary for resource search view.

        Returns:
            Dictionary of context values.
        """
        context = super().get_context_data(*args, **kwargs)

        # Get request query parmaters
        query_text = self.request.GET.get('q')
        selected_languages = self.request.GET.getlist('lang')
        selected_technological_areas = self.request.GET.getlist('tech_area')
        selected_progress_outcomes = self.request.GET.getlist('progress_outcome')
        selected_nzqa_standards = self.request.GET.getlist('nzqa_standard')
        selected_year_levels = self.request.GET.getlist('year_level')
        selected_curriculum_learning_areas = self.request.GET.getlist('curriculum_area')

        get_request = bool(self.request.GET)

        context['languages'] = Language.objects.annotate(
            selected=Case(
                When(id__in=selected_languages, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        context['technological_areas'] = TechnologicalArea.objects.annotate(
            selected=Case(
                When(id__in=selected_technological_areas, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        context['progress_outcomes'] = ProgressOutcome.objects.annotate(
            selected=Case(
                When(id__in=selected_progress_outcomes, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        context['nzqa_standards'] = NZQAStandard.objects.annotate(
            selected=Case(
                When(id__in=selected_nzqa_standards, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        context['year_levels'] = YearLevel.objects.annotate(
            selected=Case(
                When(id__in=selected_year_levels, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        context['curriculum_learning_areas'] = CurriculumLearningArea.objects.annotate(
            selected=Case(
                When(id__in=selected_curriculum_learning_areas, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        if get_request:
            context['search'] = get_request

            # Start with all objects
            results = Resource.objects.filter(published=True)

            # Filter items by tags if given in query.
            if selected_languages:
                results = results.filter(languages__in=selected_languages)
            if selected_technological_areas:
                results = results.filter(technological_areas__in=selected_technological_areas)
            if selected_progress_outcomes:
                results = results.filter(progress_outcomes__in=selected_progress_outcomes)
            if selected_nzqa_standards:
                results = results.filter(nzqa_standards__in=selected_nzqa_standards)
            if selected_year_levels:
                results = results.filter(year_levels__in=selected_year_levels)
            if selected_curriculum_learning_areas:
                results = results.filter(curriculum_learning_areas__in=selected_curriculum_learning_areas)

            # Search by text query if provided
            if query_text:
                query = SearchQuery(query_text, search_type="websearch")
                results = Resource.objects.filter(
                    search_vector=query
                ).annotate(
                    rank=SearchRank(F('search_vector'), query)
                ).filter(rank__gt=0).order_by('-rank')

            results = results.prefetch_related(
                'author_entities',
                'author_users',
                'languages',
                'technological_areas',
                'progress_outcomes',
                'nzqa_standards',
                'year_levels',
                'curriculum_learning_areas',
            ).distinct()

            context['query'] = query_text
            context['results'] = results
            context['results_count'] = len(results)
        return context


class ResourceAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows resources to be viewed."""

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
