# Generated by Django 5.1 on 2024-08-25 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_alter_crop_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crop',
            options={'ordering': ['crop_level']},
        ),
    ]
