"""Utility functions for learning area cards application."""

from urllib.parse import quote as urlquote
from django.conf import settings

ACHIEVEMENT_OBJECTIVE_TITLE_TEMPLATE = 'Achievement Objectives - Level {}'
PROGRESS_OUTCOME_TITLE_TEMPLATE = 'Progress Outcomes - {}'


def get_card_set_metadata(card_type, print_type, level=None, learning_area=None):
    """Get metadata for card set.

    Args:
        card_type (str): Type of cards in set (achievement objectives or
                         progress outcomes).
        print_type (str): Either single or double sided cards.
        level (int): Level of achievement objective.
        learning_area (str): Name of learning area for progress outcome.

    Returns:
        Tuple of string of card set title, and string of filname.
    """
    if card_type == 'ao':
        title = ACHIEVEMENT_OBJECTIVE_TITLE_TEMPLATE.format(level)
    else:
        title = PROGRESS_OUTCOME_TITLE_TEMPLATE.format(learning_area)

    filename = settings.LEARNING_AREA_CARDS_FILENAME_TEMPLATE.format(
        card_set_title=title,
        print_type=print_type,
    )
    return (title, filename)
