

# Generated by Django 5.1.6 on 2025-04-05 01:22


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_alter_artist_avatar_url_alter_artist_name_and_more'),
        ('interactions', '0003_folder_alter_userfollowedplaylist_folder_playlist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistpick',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artist_picks', to='interactions.playlist'),
        ),
    ]
