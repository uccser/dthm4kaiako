# Generated by Django 2.1.5 on 2019-03-05 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20190305_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(default='Christchurch', help_text='Town or city, for example: Christchurch', max_length=200),
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Northland'), (2, 'Auckland'), (3, 'Waikato'), (4, 'Bay of Plenty'), (5, 'Gisborne'), (6, "Hawke's Bay"), (7, 'Taranaki'), (8, 'Manawatu-Wanganui'), (9, 'Wellington'), (10, 'Tasman'), (11, 'Nelson'), (12, 'Marlborough'), (13, 'West Coast'), (14, 'Canterbury'), (15, 'Otago'), (16, 'Southland'), (17, 'Chatman Islands')], default=14),
        ),
        migrations.AddField(
            model_name='location',
            name='room',
            field=models.CharField(blank=True, help_text='Name of room or space, for example: Room 134', max_length=200),
        ),
        migrations.AddField(
            model_name='location',
            name='street_address',
            field=models.CharField(blank=True, help_text='Street address location, for example: 12 High Street', max_length=200),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(help_text='Name of location, for example: Middleton Grange School', max_length=200),
        ),
    ]
