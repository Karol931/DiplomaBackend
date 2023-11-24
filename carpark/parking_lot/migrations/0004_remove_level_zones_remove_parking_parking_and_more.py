# Generated by Django 4.2.5 on 2023-11-23 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot', '0003_rename_ispaid_parking_is_paid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='zones',
        ),
        migrations.RemoveField(
            model_name='parking',
            name='parking',
        ),
        migrations.RemoveField(
            model_name='zone',
            name='spots',
        ),
        migrations.AddField(
            model_name='level',
            name='parking',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parking_lot.parking'),
        ),
        migrations.AddField(
            model_name='spot',
            name='zone',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parking_lot.zone'),
        ),
        migrations.AddField(
            model_name='zone',
            name='level',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parking_lot.level'),
        ),
    ]