# Generated by Django 3.2.13 on 2022-05-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0041_alter_eventapplication_billing_email_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventapplication',
            name='billing_email_address',
            field=models.EmailField(default='', max_length=100),
        ),
    ]
