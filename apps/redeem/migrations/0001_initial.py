# Generated by Django 5.0.2 on 2024-03-02 19:10

import django.core.validators
import django.db.models.deletion
import utils.validates.validates
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MarketingApplican",
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
                    "date",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="Fecha"
                    ),
                ),
                (
                    "time",
                    models.TimeField(auto_now_add=True, null=True, verbose_name="Hora"),
                ),
                (
                    "place",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.MinLengthValidator(2),
                            utils.validates.validates.validate_letters_numbers_and_spaces,
                        ],
                        verbose_name="A quién se vendio",
                    ),
                ),
                (
                    "prize_fund",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=11,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Fondo de premio",
                    ),
                ),
                (
                    "winners",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Cantidad de premiados",
                    ),
                ),
                (
                    "cant_codes",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Cantidad de codigos",
                    ),
                ),
            ],
            options={
                "verbose_name": "Solicitante de marketing",
                "verbose_name_plural": "Solicitantes de marketing",
            },
        ),
        migrations.CreateModel(
            name="Code",
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
                    "prize_fund",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=11,
                        null=True,
                        verbose_name="Premio",
                    ),
                ),
                ("code", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("redeem", models.BooleanField(default=False, verbose_name="Canjeado")),
                (
                    "marketingApplican",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="marketingApplican",
                        to="redeem.marketingapplican",
                    ),
                ),
            ],
            options={
                "verbose_name": "Código",
                "verbose_name_plural": "Códigos",
            },
        ),
    ]
