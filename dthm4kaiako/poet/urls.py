"""URL routing for POET application."""

from django.urls import path
from poet import views

app_name = 'poet'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('form/', views.poet_form, name='form'),
    path('statistics/', views.StatisticsListView.as_view(), name='statistics'),
    path('statistics/<int:pk>/', views.StatisticsDetailsView.as_view(), name='statistics_detail'),
    path('contact-us/', views.ContactView.as_view(), name='contact'),
]
