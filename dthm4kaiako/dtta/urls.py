"""URL routing for DTTA application."""

from django.urls import path
from . import views

app_name = 'dtta'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('membership/', views.MembershipView.as_view(), name='membership'),
    path('news/', views.NewsArticleListView.as_view(), name='news_article_list'),
    path('news/<int:pk>/', views.NewsArticleDetailView.as_view(), name='news_article'),
]
