# Generated by Django 4.2.7 on 2023-11-27 22:22

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0024_alter_zona0manager_total_burn"),
    ]

    operations = [
        migrations.CreateModel(
            name="Map",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("map_name", models.CharField(max_length=200)),
                (
                    "map_data",
                    models.FileField(
                        storage=gdstorage.storage.GoogleDriveStorage(),
                        upload_to="maps/",
                    ),
                ),
            ],
        ),
    ]
