# Generated by Django 2.1.5 on 2020-03-07 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_entity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entity',
            options={'ordering': ['name'], 'verbose_name_plural': 'entities'},
        ),
        migrations.AlterField(
            model_name='entity',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
