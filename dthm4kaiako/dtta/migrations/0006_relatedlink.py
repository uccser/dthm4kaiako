# Generated by Django 2.1.5 on 2019-01-28 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtta', '0005_auto_20190124_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
        ),
    ]
