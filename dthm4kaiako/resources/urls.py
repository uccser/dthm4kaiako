"""URL routing for resources application."""

from django.urls import path, re_path
from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.ResourceListView.as_view(), name='home'),
    path('resource/<int:pk>/', views.ResourceDetailView.as_view(), name='resource'),
    path('resource/<int:pk>/<slug:slug>/', views.ResourceDetailView.as_view(), name='resource'),
]
