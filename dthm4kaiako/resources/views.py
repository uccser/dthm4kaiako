"""Views for resource application."""

from django.views import generic
from config.mixins import RedirectToCosmeticURLMixin
from resources.models import (
    Resource,
)


class ResourceListView(generic.ListView):
    """View for listing resources."""

    model = Resource
    context_object_name = 'resources'


class ResourceDetailView(RedirectToCosmeticURLMixin, generic.DetailView):
    """View for a resource."""

    model = Resource
    context_object_name = 'resource'
