# Generated by Django 5.1 on 2024-08-24 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kagel_crop',
            name='crop_label',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]
