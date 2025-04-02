# Generated by Django 5.1.6 on 2025-04-02 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='duration',
            new_name='duration_ms',
        ),
        migrations.AddField(
            model_name='track',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
