# Generated by Django 5.1.6 on 2025-04-02 09:26

import apps.core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='avatar_url',
            field=models.ImageField(blank=True, null=True, upload_to=apps.core.utils.generate_unique_filename),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='thumbnail_url',
            field=models.ImageField(blank=True, null=True, upload_to=apps.core.utils.generate_unique_filename),
        ),
    ]
