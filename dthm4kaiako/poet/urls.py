"""URL routing for POET application."""

from django.urls import path
from poet import views

app_name = 'poet'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('form/', views.poet_form, name='form'),
    # path('form/results/', views.poet_form, name='results'),
]
