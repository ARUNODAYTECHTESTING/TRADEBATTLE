# Generated by Django 3.2.2 on 2023-08-13 15:35

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(default='banner_image/default_image.png', upload_to='banner_image')),
                ('fees', models.IntegerField(default=0)),
                ('video_count', models.IntegerField(default=0)),
                ('enrolled_user', models.IntegerField(default=0)),
                ('extra_data', models.JSONField(blank=True, null=True)),
                ('trailer', models.CharField(blank=True, max_length=1000, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='learning.category')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('video', models.CharField(max_length=1000)),
                ('thumbnail', models.ImageField(default='lecture/default_image.png', upload_to='lecture')),
                ('views', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('extra_data', models.JSONField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.course')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(default='level_image/default_image.png', upload_to='level_image')),
                ('extra_field', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEnrolment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('course', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField()),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.lecture')),
            ],
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField()),
                ('page_no', models.IntegerField(default=1)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.lecture')),
            ],
            options={
                'ordering': ('page_no',),
                'unique_together': {('page_no', 'lecture')},
            },
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.level'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField()),
                ('correct', models.BooleanField(default=False)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.question')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('quiz_atempt', models.IntegerField(default=0)),
                ('book_page', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.userenrolment')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.lecture')),
            ],
            options={
                'unique_together': {('course', 'video')},
            },
        ),
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.pages')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('page', 'user')},
            },
        ),
    ]
