"""Module for admin configuration for the DTTA application."""

from django.contrib import admin
from dtta.models import (
    Page,
    NewsArticle,
)


class PageAdmin(admin.ModelAdmin):
    """Configuration for display DTTA flat pages in admin."""

    list_display = ('title', 'date')
    ordering = ('order_number', )


class NewsArticleAdmin(admin.ModelAdmin):
    """Configuration for display news articles in admin."""

    list_display = ('title', 'datetime')


admin.site.register(Page, PageAdmin)
admin.site.register(NewsArticle, NewsArticleAdmin)
