"""Module for factories for testing the DTTA application."""

from factory import DjangoModelFactory, Faker
from dtta.models import (
    NewsArticle,
    Page,
    RelatedLink,
)
import pytz


class NewsArticleFactory(DjangoModelFactory):
    """Factory for generating news articles."""

    title = Faker('sentence')
    content = Faker('paragraph', nb_sentences=50)
    datetime = Faker('date_time_this_decade', tzinfo=pytz.timezone('Pacific/Auckland'))

    class Meta:
        """Metadata for class."""

        model = NewsArticle


class PageFactory(DjangoModelFactory):
    """Factory for generating DTTA pages."""

    title = Faker('sentence')
    content = Faker('paragraph', nb_sentences=5)
    date = Faker('date_time_this_decade', tzinfo=pytz.timezone('Pacific/Auckland'))
    published = True

    class Meta:
        """Metadata for class."""

        model = Page


class RelatedLinkFactory(DjangoModelFactory):
    """Factory for generating DTTA related links."""

    name = Faker('url')
    url = Faker('url')

    class Meta:
        """Metadata for class."""

        model = RelatedLink
