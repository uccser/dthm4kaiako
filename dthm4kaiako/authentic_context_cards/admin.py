"""Module for admin configuration for authentic context cards application."""

from django.contrib import admin
from authentic_context_cards.models import AchivementObjective


admin.site.register(AchivementObjective)
