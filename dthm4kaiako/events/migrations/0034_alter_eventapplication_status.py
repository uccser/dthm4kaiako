# Generated by Django 3.2.13 on 2022-05-26 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0033_remove_eventapplication_usereditable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventapplication',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Rejected'), (4, 'Withdrawn')], default=1),
        ),
    ]
