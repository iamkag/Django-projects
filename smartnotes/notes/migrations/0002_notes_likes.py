# Generated by Django 5.2.1 on 2025-06-14 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='likes',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
