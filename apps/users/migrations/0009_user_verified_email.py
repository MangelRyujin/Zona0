# Generated by Django 4.2.7 on 2023-11-18 00:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_remove_user_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="verified_email",
            field=models.BooleanField(default=False, verbose_name="Verificar email"),
        ),
    ]
