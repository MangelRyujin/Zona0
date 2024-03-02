# Generated by Django 5.0.2 on 2024-03-02 19:12

from django.db import migrations
from django.contrib.auth import get_user_model

def create_user(apps,schema_editor):
    User = get_user_model()
    User.objects.create_superuser('mangel','mangelryujin@gmail.com','admin')
    

class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_user),
    ]
