# Generated by Django 3.2.14 on 2022-07-16 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0060_eventapplication_bill_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventapplication',
            name='bill_to',
            field=models.CharField(default='', help_text='Who will be paying for this participant to attend?', max_length=200),
        ),
    ]