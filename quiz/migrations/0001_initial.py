# Generated by Django 4.1.7 on 2024-01-09 17:47

import ckeditor_uploader.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('class_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('course_name', models.CharField(max_length=50)),
                ('question_number', models.PositiveIntegerField()),
                ('total_marks', models.PositiveIntegerField()),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseClassTime',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('times', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('marks', models.PositiveIntegerField()),
                ('question', ckeditor_uploader.fields.RichTextUploadingField()),
                ('variant_A', ckeditor_uploader.fields.RichTextUploadingField(default='A')),
                ('variant_B', ckeditor_uploader.fields.RichTextUploadingField(default='B')),
                ('variant_C', ckeditor_uploader.fields.RichTextUploadingField(default='C')),
                ('variant_D', ckeditor_uploader.fields.RichTextUploadingField(default='D')),
                ('answer', models.CharField(choices=[('variant_A', 'A'), ('variant_B', 'B'), ('variant_C', 'C'), ('variant_D', 'D')], max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RandomQuestionMarks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('marks', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('marks', models.PositiveIntegerField()),
                ('question_results', models.JSONField(null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('c_marks', models.PositiveIntegerField(default=100)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.classes')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
