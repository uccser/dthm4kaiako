"""Module for factories for tesing DTTA application."""

from factory import DjangoModelFactory, Faker
from dtta.models import NewsArticle
import pytz


class NewsArticleFactory(DjangoModelFactory):
    """Factory for generating news articles."""

    title = Faker('sentence')
    content = Faker('paragraph', nb_sentences=50)
    datetime = Faker('date_time_this_decade', tzinfo=pytz.timezone('Pacific/Auckland'))

    class Meta:
        """Metadata for class."""

        model = NewsArticle
