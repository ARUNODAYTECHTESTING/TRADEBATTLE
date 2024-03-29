# Generated by Django 4.2.1 on 2023-07-04 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0003_watchlist_book_page"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={"ordering": ("name",),},
        ),
        migrations.AddField(
            model_name="level", name="extra_field", field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name="course",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="learning.category",
            ),
        ),
    ]
