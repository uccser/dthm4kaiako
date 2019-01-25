"""URL routing for resources application."""

from django.urls import path, re_path
from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.ResourceListView.as_view(), name='home'),
    re_path(r'^resource/(?P<pk>\d+)/((?P<slug>[-\w]+)/)?$', views.ResourceDetailView.as_view(), name='resource'),
]
