# Generated by Django 2.1.5 on 2019-07-31 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poet', '0004_auto_20190801_1142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='progressoutcome',
            options={'ordering': ['label']},
        ),
    ]
