"""Views for resource application."""

from django.views import generic
from resources.models import (
    Resource,
)


class ResourceListView(generic.ListView):
    """View for listing resources."""

    model = Resource
    context_object_name = 'resources'


class ResourceDetailView(generic.DetailView):
    """View for a resource."""

    model = Resource
    context_object_name = 'resource'
