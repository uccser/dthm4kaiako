# Generated by Django 3.2.15 on 2022-09-10 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0094_auto_20220910_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Participant type e.g. teacher, event staff', max_length=200)),
                ('price', models.FloatField(help_text='Cost for participant to attend in NZD')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='ticket_types',
            field=models.ManyToManyField(related_name='tickets', to='events.Ticket'),
        ),
    ]
