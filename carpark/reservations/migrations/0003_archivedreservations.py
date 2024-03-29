# Generated by Django 4.2.5 on 2023-12-18 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot', '0008_alter_parking_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0002_rename_parking_id_reservations_parking_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedReservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('parking', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parking_lot.parking')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
