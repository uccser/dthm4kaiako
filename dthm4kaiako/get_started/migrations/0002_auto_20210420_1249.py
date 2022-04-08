# Generated by Django 2.2.18 on 2021-04-20 00:49

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_started', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='published',
        ),
        migrations.AddField(
            model_name='component',
            name='video_transcript',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AddField(
            model_name='component',
            name='video_url',
            field=models.URLField(blank=True),
        ),
    ]
