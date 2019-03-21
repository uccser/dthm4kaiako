"""URL routing for resources application."""

from django.urls import path
# from rest_framework import routers
from . import views

app_name = 'resources'

# router = routers.DefaultRouter()
# router.register(r'api', views.ResourceAPIViewSet)

urlpatterns = [
    path('', views.ResourceHomeView.as_view(), name='home'),
    # path('', include(router.urls)),
    path('resource/<int:pk>/', views.ResourceDetailView.as_view()),
    path('resource/<int:pk>/<slug:slug>/', views.ResourceDetailView.as_view(), name='resource'),
    path('search/', views.ResourceSearchView.as_view(), name='search'),
]
