# Generated by Django 4.2.7 on 2024-01-08 14:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0027_user_image"),
    ]

    operations = [
        migrations.DeleteModel(
            name="AvatarImageUser",
        ),
    ]
