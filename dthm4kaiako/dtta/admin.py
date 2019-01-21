"""Module for admin configuration for the DTTA application."""

from django.db import models
from django.contrib import admin
from dtta.models import NewsArticle
from martor.widgets import AdminMartorWidget

class NewsArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(NewsArticle, NewsArticleAdmin)
