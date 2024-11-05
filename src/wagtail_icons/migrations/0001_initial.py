# Generated by Django 5.1.1 on 2024-10-02 20:47

import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Icon",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("label", models.CharField(max_length=255)),
                ("svg", models.TextField()),
                ("provider", models.CharField(max_length=255)),
                ("style", models.CharField(max_length=255)),
                ("aliases", models.CharField(max_length=511, blank=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["name", "provider", "style"],
                        name="wagtail_ico_name_9488e2_idx",
                    ),
                    models.Index(
                        fields=["provider", "style"],
                        name="wagtail_ico_provide_7efa47_idx",
                    ),
                ],
                "unique_together": {("name", "provider", "style")},
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
