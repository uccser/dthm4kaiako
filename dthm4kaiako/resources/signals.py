# Based off https://simonwillison.net/2017/Oct/5/django-postgresql-faceted-search/

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Value
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from resources.models import (
    Resource,
)
import operator


SEARCH_INDEX_UPDATE_MODELS = (
    Resource,
)


@receiver(post_save)
def on_save(sender, **kwargs):
    if issubclass(sender, SEARCH_INDEX_UPDATE_MODELS):
        transaction.on_commit(make_updater(kwargs['instance']))


# TODO: Update on M2M relationships
# @receiver(m2m_changed)
# def on_m2m_changed(sender, **kwargs):
#     instance = kwargs['instance']
#     model = kwargs['model']
#     if model is Tag:
#         transaction.on_commit(make_updater(instance))
#     elif isinstance(instance, Tag):
#         for obj in model.objects.filter(pk__in=kwargs['pk_set']):
#             transaction.on_commit(make_updater(obj))


def make_updater(instance):
    components = instance.index_contents()
    pk = instance.pk

    def on_commit():
        search_vector_list = []
        for weight, text in components.items():
            search_vector_list.append(
                SearchVector(Value(text), weight=weight)
            )
        search_vectors = search_vector_list[0]
        for search_vector in search_vector_list[1:]:
            search_vectors += search_vector

        instance.__class__.objects.filter(pk=pk).update(
            search_vector=search_vectors
        )

    return on_commit
