# Generated by Django 4.2.1 on 2023-07-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0005_alter_pages_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="userenrolment",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
