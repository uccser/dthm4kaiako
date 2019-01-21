"""Module for admin configuration for the DTTA application."""

from django.contrib import admin
from dtta.models import NewsArticle
from markdownx.admin import MarkdownxModelAdmin


class NewsArticleAdmin(MarkdownxModelAdmin):
    """Configuration for display news articles in admin."""

    list_display = ('title', 'datetime')


admin.site.register(NewsArticle, NewsArticleAdmin)
