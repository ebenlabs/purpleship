# Generated by Django 4.2.16 on 2025-02-10 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0081_freightcomsettings_api_key"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="freightcomsettings",
            name="password",
        ),
        migrations.RemoveField(
            model_name="freightcomsettings",
            name="username",
        ),
    ]
