# Generated by Django 5.1.6 on 2025-04-15 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_rename_duration_track_duration_ms_track_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='avatar_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
