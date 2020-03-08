# Generated by Django 2.1.5 on 2020-03-06 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20200225_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='registration_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Register to attend event'), (2, 'Apply to attend event'), (3, 'Visit event website'), (4, 'This event is invite only')], default=1),
        ),
    ]
