# Generated by Django 4.1.1 on 2022-09-10 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=50), max_length=200),
        ),
    ]
