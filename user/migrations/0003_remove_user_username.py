# Generated by Django 4.2.7 on 2024-03-28 11:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_user_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]