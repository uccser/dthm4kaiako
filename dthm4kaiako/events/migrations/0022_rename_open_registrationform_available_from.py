# Generated by Django 3.2.12 on 2022-04-19 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20220419_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrationform',
            old_name='open',
            new_name='available_from',
        ),
    ]