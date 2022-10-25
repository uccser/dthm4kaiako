# Generated by Django 3.2.12 on 2022-04-19 01:15

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0019_auto_20220406_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.PositiveSmallIntegerField(default=0)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_types', to='events.event')),
            ],
            options={
                'verbose_name_plural': 'application type',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RegistrationForm',
            fields=[
                ('open_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('terms_and_conditions', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='registration_form', serialize=False, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Rejected')], default=1)),
                ('staff_comments', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('paid', models.BooleanField()),
                ('application_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='events.applicanttype')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'event applications',
                'ordering': ['event', 'status'],
            },
        ),
    ]
