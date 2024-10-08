# Generated by Django 5.1 on 2024-08-24 08:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_nitrogen', models.FloatField(blank=True, null=True)),
                ('crop_phosphorous', models.FloatField(blank=True, null=True)),
                ('crop_potassium', models.FloatField(blank=True, null=True)),
                ('crop_temperature', models.FloatField(blank=True, null=True)),
                ('crop_rainfall', models.FloatField(blank=True, null=True)),
                ('crop_humidity', models.FloatField(blank=True, null=True)),
                ('crop_ph', models.FloatField(blank=True, null=True)),
                ('crop_level', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='kagel_crop',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_path', models.CharField(blank=True, max_length=100, null=True)),
                ('crop_label', models.CharField(blank=True, max_length=100, null=True)),
                ('crop_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.crop')),
            ],
        ),
    ]
