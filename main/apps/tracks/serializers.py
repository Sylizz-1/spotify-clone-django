from rest_framework import serializers

from apps.artists.serializers import ArtistSerializer
from .models import Track, TrackArtist
from apps.artists.models import Artist
from apps.albums.models import Album
from apps.albums.serializers import AlbumSerializer

class TrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)  # Assuming you want to show artist details
    album = AlbumSerializer(read_only=True)  # Assuming you want to show album details
    
    class Meta:
        model = Track
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': False},
            'avatar_url': {'required': False},
            'is_public': {'required': False},
            'likes_count': {'required': False},
            'artist': {'required': False},  # Assuming artist is required
            'album': {'required': False},  # Assuming album is required
        }
    def validate_audio_file_path(self, value):
        # Validate file extension
        if not value.name.lower().endswith('.mp3'):
            raise serializers.ValidationError('Only MP3 files are allowed')

        # Validate file size (2B)
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError('File size too large. Maximum size is 20MB')

        return value

class TrackArtistSerializer(serializers.ModelSerializer):
    # artist = serializers.StringRelatedField()  # or use a nested serializer if needed
    artist = ArtistSerializer()
    
    class Meta:
        model = TrackArtist
        fields = '__all__'
