# Generated by Django 4.2.7 on 2024-01-22 20:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("redeem", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="marketingapplican",
            name="prize_fund",
            field=models.DecimalField(
                decimal_places=2,
                default=1,
                max_digits=11,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Fondo de premio",
            ),
        ),
    ]
