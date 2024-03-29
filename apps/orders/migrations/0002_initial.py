# Generated by Django 5.0.2 on 2024-03-02 19:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orders", "0001_initial"),
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="receiveosp",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="transfermanagerorderusers",
            name="user_manager",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.zona0manager"
            ),
        ),
        migrations.AddField(
            model_name="transferosp",
            name="receive",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="orders.receiveosp"
            ),
        ),
        migrations.AddField(
            model_name="transferosp",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
