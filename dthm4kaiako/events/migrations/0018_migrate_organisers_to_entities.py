from django.db import migrations, models


def migrate_data_to_entities(apps, schema_editor):
    # Existing models
    Organiser = apps.get_model('events', 'Organiser')
    Sponsor = apps.get_model('events', 'Sponsor')
    Event = apps.get_model('events', 'Event')
    # New model
    Entity = apps.get_model('users', 'Entity')
    # Duplicate old objects as new model objects
    for organiser in Organiser.objects.order_by('pk'):
        Entity.objects.get_or_create(
            name=organiser.name,
            defaults={'url': organiser.url},
        )
    for sponsor in Sponsor.objects.all():
        Entity.objects.get_or_create(
            name=sponsor.name,
            defaults={'url': sponsor.url},
        )
    # For every event, recreate relationship links
    for event in Event.objects.all():
        for organiser in event.organisers.all():
            organiser_as_entity = Entity.objects.get(name=organiser.name)
            event.organisers_new.add(organiser_as_entity)
        for sponsor in event.sponsors.all():
            sponsor_as_entity = Entity.objects.get(name=sponsor.name)
            event.sponsors_new.add(sponsor_as_entity)


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20200306_1434'),
        ('users', '0006_auto_20200307_2336'),
    ]

    operations = [
        # Add new fields to event
        migrations.AddField(
            model_name='event',
            name='organisers_new',
            field=models.ManyToManyField(blank=True, related_name='events', to='users.Entity'),
        ),
        migrations.AddField(
            model_name='event',
            name='sponsors_new',
            field=models.ManyToManyField(blank=True, related_name='sponsored_events', to='users.Entity'),
        ),
        # Change Python to duplicate relationships
        migrations.RunPython(migrate_data_to_entities),
        # Remove old fields
        migrations.RemoveField(
            model_name='event',
            name='organisers',
        ),
        migrations.RemoveField(
            model_name='event',
            name='sponsors',
        ),
        # Remove models
        migrations.DeleteModel(
            name='Organiser',
        ),
        migrations.DeleteModel(
            name='Sponsor',
        ),
        # Rename fields
        migrations.RenameField(
            model_name='event',
            old_name='organisers_new',
            new_name='organisers',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='sponsors_new',
            new_name='sponsors',
        ),
    ]
