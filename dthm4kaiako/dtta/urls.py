"""URL routing for DTTA application."""

from django.urls import path
from . import views

app_name = 'dtta'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news/<int:pk>/', views.NewsArticleDetailView.as_view(), name='news_article'),
]
