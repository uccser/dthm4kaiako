# Generated by Django 3.2.12 on 2022-04-08 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtta', '0013_auto_20220406_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='page_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Planning'), (2, 'Documents')], default=1),
        ),
    ]
