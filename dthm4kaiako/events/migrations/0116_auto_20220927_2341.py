# Generated by Django 3.2.15 on 2022-09-27 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0115_alter_deletedeventapplication_deletion_reason'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deletedeventapplication',
            name='deletion_reason',
        ),
        migrations.AddField(
            model_name='deletedeventapplication',
            name='withdraw_reason',
            field=models.PositiveSmallIntegerField(choices=[(3, 'No longer interested'), (4, 'Change of plans'), (5, 'No funding'), (6, 'Inconvient location'), (8, 'Wrong event'), (9, 'Clash of personal development'), (2, 'Illness'), (1, 'Prefer not to say'), (7, 'Other')], default=1, help_text='Reason the participant has chosen to withdraw their application.'),
        ),
    ]