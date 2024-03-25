# Generated by Django 5.0.3 on 2024-03-25 15:38

import apps.users.models
import django.core.validators
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_profile_about"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="about",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="default.png",
                upload_to=apps.users.models.Profile.get_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(["png", "jpg"])
                ],
            ),
        ),
    ]
