# Generated by Django 3.2.12 on 2022-04-06 03:51

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0011_install_extensions'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='resource',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='resources_r_search__82e125_gin'),
        ),
    ]
