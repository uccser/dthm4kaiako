# Generated by Django 3.2.13 on 2022-05-31 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0044_auto_20220531_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationform',
            name='close_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registrationform',
            name='open_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
