from django.contrib import admin
from dtta.models import NewsArticle
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(NewsArticle, MarkdownxModelAdmin)
