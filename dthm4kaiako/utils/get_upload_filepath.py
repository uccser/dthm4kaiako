"""Helper functions for determining file paths for uploads."""

from os.path import join
from datetime import datetime
from pytz import timezone

# This is duplicated here to avoid circular dependency with settings file
TIME_ZONE = 'NZ'


def get_upload_path_for_date(category):
    """Create upload path for file by date.

    Args:
        category (str): Name for directory to upload to.

    Returns:
        String of path for upload.
    """
    return join(category, datetime.now(timezone(TIME_ZONE)).strftime('%Y/%m/%d'))


def get_resource_upload_path(component, filename):
    """Create upload path for resource by primary key.

    Required by model FileField/ImageField.

    Args:
        component (ResourceComponent): Component object file is being added to.
        filename (str): Filename of file.

    Returns:
        String of path and filename for upload.
    """
    return join('resources', str(component.resource.pk), filename)


def get_event_organiser_upload_path(organiser, filename):
    """Create upload path for an event organiser by primary key.

    Required by model FileField/ImageField.

    Args:
        component (Organiser): Organiser object file is being added to.
        filename (str): Filename of file.

    Returns:
        String of path and filename for upload.
    """
    return join('events', 'organiser', str(organiser.pk), filename)


def get_event_sponsor_upload_path(organiser, filename):
    """Create upload path for an event sponsor by primary key.

    Required by model FileField/ImageField.

    Args:
        component (Sponsor): Sponsor object file is being added to.
        filename (str): Filename of file.

    Returns:
        String of path and filename for upload.
    """
    return join('events', 'sponsor', str(organiser.pk), filename)


def get_event_series_upload_path(series, filename):
    """Create upload path for an event series by primary key.

    Required by model FileField/ImageField.

    Args:
        component (Series): Series object file is being added to.
        filename (str): Filename of file.

    Returns:
        String of path and filename for upload.
    """
    return join('events', 'series', str(series.pk), filename)


def get_dtta_news_article_source_upload_path(source, filename):
    """Create upload path for a DTTA news source logo.

    Required by model ImageField.

    Args:
        source (NewsArticleSource): News article source object file is being added to.
        filename (str): Filename of file.

    Returns:
        String of path and filename for upload.
    """
    return join('dtta', 'news-article-source', str(source.slug), filename)
