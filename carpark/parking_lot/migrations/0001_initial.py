# Generated by Django 4.2.5 on 2023-11-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('isTaken', models.BooleanField(max_length=50)),
                ('user_id', models.IntegerField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1)),
                ('spots', models.ManyToManyField(related_name='zones', to='parking_lot.spot')),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('isPaid', models.BooleanField()),
                ('parking', models.ManyToManyField(related_name='parking', to='parking_lot.level')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='zones',
            field=models.ManyToManyField(related_name='levels', to='parking_lot.zone'),
        ),
    ]
