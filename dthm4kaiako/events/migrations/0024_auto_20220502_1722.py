# Generated by Django 3.2.12 on 2022-05-02 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20220502_1633'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start', 'end']},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['start', 'end', 'name']},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='end_datetime',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='start_datetime',
            new_name='start',
        ),
        migrations.RenameField(
            model_name='registrationform',
            old_name='end_datetime',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='registrationform',
            old_name='open_datetime',
            new_name='open',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='end_datetime',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='start_datetime',
            new_name='start',
        ),
        migrations.AlterField(
            model_name='eventapplication',
            name='userEditable',
            field=models.BooleanField(),
        ),
    ]
