# Generated by Django 4.1.7 on 2024-01-02 14:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseclasstime',
            name='times',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(200)]),
        ),
    ]