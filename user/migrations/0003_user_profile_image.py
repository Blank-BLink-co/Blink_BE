# Generated by Django 5.0 on 2024-02-05 00:35

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_profile_image.jpg', null=True, upload_to=user.models.image_upload_path),
        ),
    ]
