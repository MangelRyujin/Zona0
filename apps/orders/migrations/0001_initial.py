# Generated by Django 4.2.7 on 2023-11-18 15:19

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
            name="TransferOrderUsers",
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
                (
                    "cant_zona_point",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Puntos de Zona0 transferidos",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=50,
                        unique=True,
                        verbose_name="Correo Electrónico del usuario al que se le transfirió",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
