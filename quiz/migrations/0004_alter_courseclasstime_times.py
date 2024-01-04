# Generated by Django 4.1.7 on 2024-01-03 04:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_courseclasstime_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseclasstime',
            name='times',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)]),
        ),
    ]
