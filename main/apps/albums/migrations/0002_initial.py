# Generated by Django 5.1.6 on 2025-03-21 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='artists.artist'),
        ),
        migrations.AddField(
            model_name='albumartist',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributing_artists', to='albums.album'),
        ),
        migrations.AddField(
            model_name='albumartist',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album_credits', to='artists.artist'),
        ),
        migrations.AlterUniqueTogether(
            name='albumartist',
            unique_together={('artist', 'album', 'role')},
        ),
    ]
