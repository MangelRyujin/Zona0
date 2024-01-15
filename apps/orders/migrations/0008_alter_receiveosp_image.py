# Generated by Django 4.2.7 on 2024-01-09 04:01

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0007_receiveosp_transferosp_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receiveosp",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=gdstorage.storage.GoogleDriveStorage(),
                upload_to="avatar/",
            ),
        ),
    ]