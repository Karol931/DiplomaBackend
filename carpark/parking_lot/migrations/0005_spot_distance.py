# Generated by Django 4.2.5 on 2023-12-13 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot', '0004_remove_level_zones_remove_parking_parking_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='distance',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]