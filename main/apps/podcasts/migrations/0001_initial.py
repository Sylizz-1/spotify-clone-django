# Generated by Django 5.1.6 on 2025-03-21 09:22

import apps.core.utils
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('public_web_url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('author_name', models.CharField(max_length=255)),
                ('copyright_notice', models.CharField(blank=True, max_length=255)),
                ('cover_art_image_url', models.ImageField(upload_to=apps.core.utils.generate_unique_filename)),
                ('thumbnail_url', models.ImageField(upload_to=apps.core.utils.generate_unique_filename)),
                ('description', models.JSONField(default=dict)),
                ('rss_feed_url', models.URLField(blank=True)),
                ('rss_feed_file', models.FileField(blank=True, upload_to=apps.core.utils.generate_unique_filename)),
                ('licensor', models.CharField(blank=True, max_length=255)),
                ('language', models.CharField(max_length=50)),
                ('explicit', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Podcaster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bio', models.TextField(blank=True)),
                ('verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PodcastRate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PodcastEpisode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('audio_url', models.FileField(blank=True, upload_to=apps.core.utils.generate_unique_filename)),
                ('transcript_url', models.FileField(blank=True, upload_to=apps.core.utils.generate_unique_filename)),
                ('duration_seconds', models.IntegerField()),
                ('season', models.IntegerField(blank=True, null=True)),
                ('episode_number', models.IntegerField(blank=True, null=True)),
                ('explicit', models.BooleanField(default=False)),
                ('cover_art_image_url', models.ImageField(blank=True, upload_to=apps.core.utils.generate_unique_filename)),
                ('is_featured', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('full', 'Full Episode'), ('trailer', 'Trailer'), ('bonus', 'Bonus')], default='full', max_length=50)),
                ('chapters', models.JSONField(blank=True, default=dict)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=50)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('scheduled_date', models.DateTimeField(blank=True, null=True)),
                ('podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='podcasts.podcast')),
            ],
            options={
                'ordering': ['season', 'episode_number'],
            },
        ),
        migrations.CreateModel(
            name='PodcastEpisodeComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('is_public', models.BooleanField(default=True)),
                ('response_from_creator', models.TextField(blank=True)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='podcasts.podcastepisode')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
