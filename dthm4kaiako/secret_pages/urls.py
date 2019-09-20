"""URL routing for secret_pages application."""

from django.urls import path
from secret_pages import views

app_name = 'secret_pages'
urlpatterns = [
    path('<slug:slug>/', views.secret_page_view, name='page'),
]
