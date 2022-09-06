# Generated by Django 3.2.15 on 2022-09-05 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0083_auto_20220905_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='registration_link',
            field=models.URLField(blank=True, help_text="Optional. This is a link to an external location that will gather event applications' information e.g. Google Form", null=True),
        ),
    ]