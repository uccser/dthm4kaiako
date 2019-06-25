"""Module for admin configuration for learning area cards application."""

from django.contrib import admin
from learning_area_cards.models import AchievementObjective


class AchievementObjectiveAdmin(admin.ModelAdmin):
    """Configuration for displaying achievement objectives in admin."""

    list_display = ('learning_area', 'level', 'component', 'strand', 'content')
    ordering = ('learning_area', 'level', 'component', 'strand')


admin.site.register(AchievementObjective, AchievementObjectiveAdmin)
