"""Signals for the resources application.

Based off https://simonwillison.net/2017/Oct/5/django-postgresql-faceted-search/
"""


from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    m2m_changed,
)
from django.db.models import Value
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from resources.models import (
    Resource,
)


SEARCH_INDEX_UPDATE_MODELS = (
    Resource,
)


@receiver(post_save)
def on_save(sender, **kwargs):
    """Trigger functions after any model save."""
    if issubclass(sender, SEARCH_INDEX_UPDATE_MODELS):
        transaction.on_commit(make_updater(kwargs['instance']))


def on_m2m_changed(sender, **kwargs):
    """Update search indexes on m2m relationship changes.

    When a registered many to many (m2m) relationship is changed, the
    search index should be updated for models that require is.
    This only applies to the text search, filter searches are always
    up to date.

    If an object changes, any items pointing to that object also
    updates their index as the text may have changed it uses
    for indexing.
    """
    instance = kwargs['instance']
    model = kwargs['model']
    if isinstance(instance, SEARCH_INDEX_UPDATE_MODELS):
        transaction.on_commit(make_updater(instance))
    elif issubclass(model, SEARCH_INDEX_UPDATE_MODELS):
        for obj in model.objects.filter(pk__in=kwargs['pk_set']):
            transaction.on_commit(make_updater(obj))


def make_updater(instance):
    """Return function for updating search index of resource."""
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


# Register specific fields as a lot of m2m relationships exist in this website.
m2m_changed.connect(on_m2m_changed, sender=Resource.author_entities.through)
m2m_changed.connect(on_m2m_changed, sender=Resource.author_users.through)
m2m_changed.connect(on_m2m_changed, sender=Resource.languages.through)
m2m_changed.connect(on_m2m_changed, sender=Resource.technological_areas.through)
m2m_changed.connect(on_m2m_changed, sender=Resource.progress_outcomes.through)
m2m_changed.connect(on_m2m_changed, sender=Resource.nzqa_standards.through)
m2m_changed.connect(on_m2m_changed, sender=Resource.year_levels.through)
m2m_changed.connect(on_m2m_changed, sender=Resource.curriculum_learning_areas.through)
